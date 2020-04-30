# -*- coding: utf-8 -*-
"""

"""
import os
import toml

import pandas as pd

from pyomo.environ import (
    ConcreteModel,
    Set,
    Var,
    Objective,
    Constraint,
    minimize,
    NonNegativeReals,
    Expression,
    Binary,
)
from pyomo.opt import SolverFactory

with open("config.toml") as config_data:
    config = toml.load(config_data)

input_data = "input-data.xlsx"


# %% DATA
conventional = pd.read_excel(
    input_data, sheet_name="conventional", index_col=[0]
)

storage = pd.read_excel(input_data, sheet_name="storage", index_col=[0])

renewable = pd.read_excel(input_data, sheet_name="renewable", index_col=[0])

demand = pd.read_excel(input_data, sheet_name="demand", index_col=[0])

carrier = pd.read_excel(input_data, sheet_name="carrier", index_col=[0])

profiles = pd.read_excel(input_data, sheet_name="profiles", parse_dates=True)

units = pd.concat([conventional, renewable, storage], sort=False)

dt = int(config["model"]["t_resolution"])

# %% MODEL
m = ConcreteModel(name="enwajo")

# %% SETS
m.TIMESTEPS = Set(
    initialize=list(range(len(profiles)))[
        config["model"]["t_start"] : config["model"]["t_end"]
    ][::dt],
    ordered=True,
)
m.CONV = Set(initialize=conventional.index)
m.RENEW = Set(initialize=renewable.index)
m.STOR = Set(initialize=storage.index)
m.ALL = m.CONV | m.RENEW


# %% VARIABLES
def p_bounds(m, t, u):
    """ Bound of supply variable p for conventional units
    """
    return (0, units.at[u, "p_nom"])


# supply variable p of all units
m.p = Var(m.TIMESTEPS, m.ALL, bounds=p_bounds)


def s_out_bounds(m, t, s):
    """ Bounds of output variable for storage units
    """
    return (0, storage.at[s, "p_nom_out"])


# storage output variable
m.s_out = Var(m.TIMESTEPS, m.STOR, bounds=s_out_bounds)


def s_in_bounds(m, t, s):
    """ Bounds of input variable for storage units
    """
    return (0, storage.at[s, "p_nom_in"])


# storage input variable
m.s_in = Var(m.TIMESTEPS, m.STOR, bounds=s_in_bounds)


def level_bounds(m, t, s):
    """ Bounds of storage filling level variable
    """
    return (0, storage.at[s, "l_nom"])


# storage level variable
m.s_level = Var(m.TIMESTEPS, m.STOR, bounds=level_bounds)

# auxiliary variable for balance constraint
m.aux = Var(m.TIMESTEPS, ["excess", "shortage"], within=NonNegativeReals)

# fix supply (p variable) of renewable energies units of the set "RENEW"
for t in m.TIMESTEPS:
    for r in m.RENEW:
        m.p[t, r].value = (
            renewable.at[r, "p_nom"]
            * profiles.at[t, renewable.at[r, "profile"]]
            * dt
        )
        m.p[t, r].fix()

# binary status variable to indicate whether unit is on / off for conv Units
m.y = Var(m.TIMESTEPS, m.CONV, within=Binary)


def opex(m, u):
    """ Expression to collect operational expenditures used in objective
    function.
    """
    if u in m.CONV:
        opex = (
            sum(
                (
                    m.p[t, u]
                    / units.at[u, "eta"]
                    * carrier.at[units.at[u, "carrier"], "cost"]
                )
                + units.at[u, "vom"]
                for t in m.TIMESTEPS
            )
            * dt
        )
    if u in m.STOR:
        opex = sum(storage.at[u, "vom"] for t in m.TIMESTEPS) * dt
    if u in m.RENEW:
        opex = sum(renewable.at[u, "vom"] for t in m.TIMESTEPS) * dt

    return opex


m.opex = Expression(m.ALL | m.STOR, rule=opex)


# %% OBJECTIVE
def obj_rule(m):
    """ Objective function of total cost
    """
    expr = 0
    expr += sum(m.opex[u] for u in m.ALL | m.STOR)
    expr += sum(m.aux[t, "shortage"] * 3000 * dt for t in m.TIMESTEPS)
    return expr


m.objective = Objective(sense=minimize, rule=obj_rule)


# %% CONSTRAINTS
def electricity_balance(m, t):
    """ Energy balance constraint
    """
    lhs = 0
    lhs += sum(m.p[t, c] for c in m.CONV)
    lhs += sum(m.p[t, r] for r in m.RENEW)
    lhs += m.aux[t, "shortage"]
    lhs += -m.aux[t, "excess"]
    lhs += sum(m.s_out[t, s] - m.s_in[t, s] for s in m.STOR)
    rhs = (
        demand.at["demand", "amount"]
        * profiles.at[t, demand.at["demand", "profile"]]
    )
    return lhs == rhs


# constraint for electricity balance
m.electricity_balance = Constraint(m.TIMESTEPS, rule=electricity_balance)


def p_min_constraint(m, t, c):
    """ Minimal supply constraint of unit
    """
    expr = m.p[t, c] >= units.at[c, "p_min"] * units.at[c, "p_nom"] * m.y[t, c]
    return expr


def p_max_constraint(m, t, c):
    """ Maximum supply constraint of unit (required for pmin to work)
    """
    return m.p[t, c] <= units.at[c, "p_max"] * units.at[c, "p_nom"] * m.y[t, c]


if config["constraints"]["pmin"]:
    m.p_min_constraint = Constraint(m.TIMESTEPS, m.CONV, rule=p_min_constraint)
    m.p_max_constraint = Constraint(m.TIMESTEPS, m.CONV, rule=p_max_constraint)

# storage balance
def storage_balance(m, t, s):
    """ Storage balance, first and last timestep are linked
    """
    if t == m.TIMESTEPS.first():
        return m.s_level[t, s] == m.s_level[m.TIMESTEPS.last(), s]
    else:
        return (
            m.s_level[t, s]
            == m.s_level[t - 1 * dt, s]
            + storage.at[s, "eta_in"] * m.s_in[t, s] * dt
            - m.s_out[t, s] / storage.at[s, "eta_out"] * dt
        )


m.storage_balance = Constraint(m.TIMESTEPS, m.STOR, rule=storage_balance)


# %% SOLVING
# m.write('problem.lp', io_options={'symbolic_solver_labels':False})

# set solver (can use other solver e.g. 'gurobi' if gurobi is installed)
opt = SolverFactory(config["model"]["solver"])

# solve model
# tee=True streams solver standard output in console
meta_results = opt.solve(m, tee=True)


# %% POSTPROCESSING
results_data = {i.name: i.get_values() for i in m.component_objects(Var)}

# store results in dataframe
supply_results = pd.Series(results_data["p"]).unstack()
supply_results = pd.concat(
    [supply_results, pd.Series(results_data["s_out"]).unstack()],
    axis=1,
    sort=False,
)

filling_levels = pd.Series(results_data["s_level"]).unstack()

demand_results = pd.Series(results_data["s_in"]).unstack()

demand_results["demand"] = (
    demand.at["demand", "amount"] * profiles[demand.at["demand", "profile"]]
).values[config["model"]["t_start"] : config["model"]["t_end"]][::dt]

cost = pd.DataFrame.from_dict(
    {k: v() for k, v in m.opex.items()}, orient="index"
)

# write to csv
if not os.path.exists("results"):
    os.makedirs("results")
filling_levels.to_csv("results/filling_levels.csv")
supply_results.to_csv("results/supply.csv")
demand_results.to_csv("results/demand.csv")
cost.to_csv("results/cost.csv")
