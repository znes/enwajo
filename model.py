# -*- coding: utf-8 -*-
"""

"""
import os
import pandas as pd

from pyomo.environ import (
    ConcreteModel, Param, Set, Var, Objective, Constraint, minimize,
    NonNegativeReals, Binary
)
from pyomo.opt import SolverFactory

input_data = "data-input.xlsx"

# %% DATA
conventionals = pd.read_excel(
    input_data, sheet_name="conventionals", index_col=[0]
)

storages = pd.read_excel(
    input_data, sheet_name="storage", index_col=[0]
)

renewables = pd.read_excel(
    input_data, sheet_name="renewables", index_col=[0]
)

demands = pd.read_excel(
    input_data, sheet_name="demand", index_col=[0]
)

profiles = pd.read_excel(
    input_data, sheet_name="profiles", parse_dates=True
)

units = pd.concat([conventionals, renewables, storages], sort=False)

t_start = 0
t_end = 168

# %% MODEL
m = ConcreteModel(name="power-model")

# %% SETS
m.TIMESTEPS = Set(initialize=list(range(len(profiles)))[t_start: t_end],
                  ordered=True)
m.CONV = Set(initialize=conventionals.index)
m.RENEW = Set(initialize=renewables.index)
m.STORAGES = Set(initialize=storages.index)
m.ALLUNITS = m.CONV | m.RENEW


# %% VARIABLES
def p_bounds(m, t, u):
    """ Bound of p variable for conventional units
    """
    return (0, units.at[u, "p_max"])
m.p = Var(m.TIMESTEPS, m.ALLUNITS, bounds=p_bounds)

def s_out_bounds(m, t, s):
    """ Bounds of storage outputs variable for storage units
    """
    return (0, storages.at[s, "p_max_out"])
m.s_out = Var(m.TIMESTEPS, m.STORAGES, bounds=s_out_bounds)

def s_in_bounds(m, t, s):
    return (0, storages.at[s, "p_max_in"])
m.s_in = Var(m.TIMESTEPS, m.STORAGES, bounds=s_in_bounds)

def level_bounds(m, t, s):
    return (0, storages.at[s, "storage_capacity"])
m.s_level = Var(m.TIMESTEPS, m.STORAGES, bounds=level_bounds)

# auxiliary variable for balance constraint
m.aux = Var(m.TIMESTEPS, ["excess", "shortage"], within=NonNegativeReals)

for t in m.TIMESTEPS:
    for r in m.RENEW:
        m.p[t, r].value = (
            renewables.at[r, "p_max"] *
            profiles.at[t, renewables.at[r, "profile"]])
        m.p[t, r].fix()

m.y = Var(m.TIMESTEPS, m.CONV, within=Binary)


# %% OBJECTIVE
def obj_rule(m):
  expr  = 0
  expr += sum(
          m.p[t, u] * units.at[u, "marginal_cost"]
          for t in m.TIMESTEPS
          for u in m.ALLUNITS
  )
  expr += sum(m.aux[t, "shortage"] * 3000 for t in m.TIMESTEPS)
  expr += sum(m.s_out[t, s] * storages.at[s, "vom"]
              for t in m.TIMESTEPS for s in m.STORAGES)
  return expr
m.objective = Objective(sense=minimize, rule=obj_rule)


# %% CONSTRAINTS
def demand_rule(m, t):
    lhs = 0
    lhs += sum(m.p[t, c] for c in m.CONV)
    lhs += sum(m.p[t, r] for r in m.RENEW)
    lhs += m.aux[t, "shortage"]
    lhs += -m.aux[t, "excess"]
    lhs += sum(m.s_out[t, s]- m.s_in[t, s] for s in m.STORAGES)
    rhs = (demands.at["demand", "amount"] *
           profiles.at[t, demands.at["demand", "profile"]])
    return lhs == rhs
m.demand_constr = Constraint(m.TIMESTEPS, rule=demand_rule)

def p_min_constraint(m, t, c):
       return m.p[t, c] >= units.at[c, "p_min"] * units.at[c, "p_max"] * m.y[t, c]
m.p_min_constraint = Constraint(m.TIMESTEPS, m.CONV, rule=p_min_constraint)

def p_max_constraint(m, t, c):
       return m.p[t, c] <= units.at[c, "p_max"] * m.y[t, c]
m.p_max_constraint = Constraint(m.TIMESTEPS, m.CONV, rule=p_max_constraint)

# storage balance
def storage_balance (m, t, s):
    if t == m.TIMESTEPS.first():
       return m.s_level[t, s] == m.s_level[m.TIMESTEPS.last(), s]
    else:
        return (
            m.s_level[t, s] ==
            m.s_level[t - 1, s] +
            storages.at[s, "eta_in"] * m.s_in[t, s] -
            m.s_out[t, s] / storages.at[s, "eta_out"]
        )
m.storage_balance = Constraint(m.TIMESTEPS, m.STORAGES,
                               rule=storage_balance)


# %% SOLVING
# m.write('problem.lp', io_options={'symbolic_solver_labels':False})

# set solver (can use other solver e.g. 'gurobi' if gurobi is installed)
opt = SolverFactory('cbc')

# solve model
# tee=True streams solver standard output in console
meta_results = opt.solve(m, tee=True)


# %% POSTPROCESSING
results_data = {i.name: i.get_values()
                for i in m.component_objects(Var)}

# store results in dataframe
supply = pd.Series(results_data["p"]).unstack()
supply = pd.concat([supply, pd.Series(results_data["s_out"]).unstack()],
                   axis=1, sort=False)

filling_levels = pd.Series(results_data["s_level"]).unstack()

demand = pd.Series(results_data["s_in"]).unstack()
demand["demand"] = (
        demands.at["demand", "amount"] *
        profiles[demands.at["demand", "profile"]]).values[t_start: t_end]

# write to csv
if not os.path.exists("results"):
    os.makedirs("results")
filling_levels.to_csv("results/filling_levels.csv")
supply.to_csv("results/supply.csv")
demand.to_csv("results/demand.csv")
# %% PLOTTING


import matplotlib.pyplot as plt
# sorted supply
sorted_supply = pd.DataFrame(
        {c: supply[c].sort_values().values for c in supply.columns})
plt.figure()
sorted_supply.plot(style="--", grid=True)
plt.ylabel("Power")
plt.xlabel("Hour")
plt.savefig("results/sorted.pdf")

# aggregated supply
fig, ax = plt.subplots()
aggr = supply.sum() / 1e6
ax = aggr.plot(kind="bar")
ax.set_title("Aggregated supply by technology in TWh")
ax.set_ylabel("Energy in TWh")
plt.xticks(rotation=45)
plt.savefig("results/aggregated_supply.pdf")
