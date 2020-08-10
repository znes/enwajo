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

from plotting import create_plots


def run(scenario="scenarios/test-scenario"):
    """
    """
    with open(os.path.join(scenario, "config.toml")) as config_data:
        config = toml.load(config_data)

    if (
        config["constraints"]["eta_partial"]
        and not config["constraints"]["pmin"]
    ):
        raise ValueError(
            "If you set `eta_partial`, you also need to set `p_min` in "
            "the config.toml file."
        )

    # set input data file
    input_data = os.path.join(scenario, config["model"]["input"], "input.xlsx")

    # result dir
    rdir = os.path.join(scenario, config["model"]["output"])
    # write results
    if not os.path.exists(rdir):
        os.makedirs(rdir)
    else:
        user_input = (
            input(
                "Output directory {} exists. Continue and overwrite "
                "(y/[n]):".format(rdir)
            )
            or "n"
        )

        if user_input != "y":
            print("Stopping process!")
            sys.exit()

    print("Reading data from `{}`".format(input_data))
    # %% DATA
    conventional = pd.read_excel(
        input_data, sheet_name="conventional", index_col=[0]
    )

    storage = pd.read_excel(input_data, sheet_name="storage", index_col=[0])

    renewable = pd.read_excel(
        input_data, sheet_name="renewable", index_col=[0]
    )

    demand = pd.read_excel(input_data, sheet_name="demand", index_col=[0])

    carrier = pd.read_excel(input_data, sheet_name="carrier", index_col=[0])

    profiles = pd.read_excel(
        input_data, sheet_name="profiles", parse_dates=True
    )

    units = pd.concat([conventional, renewable, storage], sort=False)

    dt = int(config["model"]["t_resolution"])

    # %% MODEL
    print("Building model...")

    m = ConcreteModel(name=config["name"])

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

    # fuel variable for convential power plants
    m.h = Var(m.TIMESTEPS, m.CONV, within=NonNegativeReals)

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
        if t == m.TIMESTEPS.first():
            return (
                storage.at[s, "e_nom"] * storage.at[s, "e_init"],
                storage.at[s, "e_nom"] * storage.at[s, "e_init"],
            )
        else:
            return (0, storage.at[s, "e_nom"])

    # storage level variable
    m.e = Var(m.TIMESTEPS, m.STOR, bounds=level_bounds)

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

    def fuel_consumption(m, t, u):
        """
        """
        if config["constraints"]["eta_partial"]:
            return (
                m.h[t, u]
                == (
                    m.y[t, u] * units.at[u, "a"] + m.p[t, u] * units.at[u, "b"]
                )
                * 0.2933
            )  # Mbtu -> MWh
        else:
            return m.h[t, u] == m.p[t, u] / units.at[u, "eta"]

    m.fuel_consumption = Constraint(m.TIMESTEPS, m.CONV, rule=fuel_consumption)

    def opex(m, u):
        """ Expression to collect operational expenditures used in objective
        function.
        """
        if u in m.CONV:
            opex = (
                sum(
                    (m.h[t, u] * carrier.at[units.at[u, "carrier"], "cost"])
                    + units.at[u, "vom"]
                    for t in m.TIMESTEPS
                )
                * dt
            )
        if u in m.STOR:
            opex = (
                sum(m.s_out[t, u] * storage.at[u, "vom"] for t in m.TIMESTEPS)
                * dt
            )
        if u in m.RENEW:
            opex = (
                sum(m.p[t, u] * renewable.at[u, "vom"] for t in m.TIMESTEPS)
                * dt
            )

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
        expr = (
            m.p[t, c]
            >= units.at[c, "p_min"] * units.at[c, "p_nom"] * m.y[t, c]
        )
        return expr

    def p_max_constraint(m, t, c):
        """ Maximum supply constraint of unit (required for pmin to work)
        """
        return (
            m.p[t, c]
            <= units.at[c, "p_max"] * units.at[c, "p_nom"] * m.y[t, c]
        )

    if config["constraints"]["pmin"]:
        m.p_min_constraint = Constraint(
            m.TIMESTEPS, m.CONV, rule=p_min_constraint
        )
        m.p_max_constraint = Constraint(
            m.TIMESTEPS, m.CONV, rule=p_max_constraint
        )

    # storage balance
    def storage_balance(m, t, s):
        """ Storage balance, first and last timestep are linked
        """
        if t == m.TIMESTEPS.first():
            return m.e[t, s] == m.e[m.TIMESTEPS.last(), s]
        else:
            return (
                m.e[t, s]
                == m.e[t - 1, s] * (1 - storage.at[s, "loss"])
                + storage.at[s, "eta_in"] * m.s_in[t, s] * dt
                - m.s_out[t, s] / storage.at[s, "eta_out"] * dt
            )

    m.storage_balance = Constraint(m.TIMESTEPS, m.STOR, rule=storage_balance)

    if config["model"]["debug"]:
        m.write(
            os.path.join(rdir, config["name"] + ".lp"),
            io_options={"symbolic_solver_labels": True},
        )

    # %% SOLVING
    print("Solving model...")

    # set solver (can use other solver e.g. 'gurobi' if gurobi is installed)
    opt = SolverFactory(config["model"]["solver"])

    # solve model
    # tee=True streams solver standard output in console
    meta_results = opt.solve(m, tee=config["model"]["tee"])

    # %% POSTPROCESSING
    print("Processing results...")
    results_data = {i.name: i.get_values() for i in m.component_objects(Var)}

    # store results in dataframe
    supply_results = pd.DataFrame()
    fuel_results = pd.DataFrame()
    filling_levels = pd.DataFrame()
    demand_results = pd.DataFrame()
    for var, val in results_data.items():
        if bool(val):
            if var in ["p", "s_out"]:
                supply_results = pd.concat(
                    [supply_results, pd.Series(results_data[var]).unstack()],
                    axis=1,
                    sort=False,
                )
            elif var in ["h"]:
                fuel_results = pd.concat(
                    [fuel_results, pd.Series(results_data["h"]).unstack()],
                    axis=1,
                    sort=False,
                )
            elif var == "e":
                filling_levels = pd.concat(
                    [filling_levels, pd.Series(results_data["e"]).unstack()],
                    axis=1,
                    sort=False,
                )
            elif var in ["s_in"]:
                demand_results = pd.concat(
                    [
                        demand_results,
                        pd.Series(results_data["s_in"]).unstack(),
                    ],
                    axis=1,
                    sort=False,
                )
    # add shortage and excess
    aux_df = pd.Series(results_data["aux"]).unstack()
    supply_results["shortage"] = aux_df["shortage"]
    demand_results["excess"] = aux_df["excess"]

    demand_results["demand"] = (
        demand.at["demand", "amount"]
        * profiles[demand.at["demand", "profile"]]
    ).values[config["model"]["t_start"] : config["model"]["t_end"]][::dt]

    cost = pd.DataFrame.from_dict(
        {k: v() for k, v in m.opex.items()}, orient="index"
    )
    cost.columns = ["Operational Cost"]
    cost.index.name = "Unit"

    meta_results.write(
        filename=os.path.join(rdir, "model-stats.json"), format="json"
    )

    filling_levels.to_csv(os.path.join(rdir, "filling-level.csv"))

    supply_results.to_csv(os.path.join(rdir, "supply.csv"))

    fuel_results.to_csv(os.path.join(rdir, "fuel-consumption"))

    demand_results.to_csv(os.path.join(rdir, "demand.csv"))

    cost.to_csv(os.path.join(rdir, "cost.csv"))
    print("Success! Stored results in `{}`".format(rdir))

    # generate auto  plots based on results
    plots_dir = create_plots(rdir, config)
    print("Success! Generated plots in {}".format(plots_dir))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        run()
    else:
        run(sys.argv[1])
