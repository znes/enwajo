import os
import toml

import matplotlib.pyplot as plt
from matplotlib import colors

import pandas as pd
import plotly.offline as offline


from plotly_plots import hourly_plot

with open("model-config.toml") as config_data:
    coloring = toml.load(config_data)["colors"]

# convert color names to hex for matplotlib
color_dict = {name: colors.to_hex(color) for name, color in coloring.items()}


rdir = "results"
if not os.path.exists(rdir):
    raise Exception("No result directory found to plot results.")

for dir in os.listdir(rdir):
    rfiles = os.path.join(rdir, dir) # results files path
    plots = os.path.join(rdir, dir, "plots")

    if not os.path.exists(plots):
        os.makedirs(plots)

    supply = pd.read_csv(
        os.path.join(rfiles, "supply.csv"), index_col=[0])

    demand = pd.read_csv(
        os.path.join(rfiles, "demand.csv"), index_col=[0])

    all = pd.concat([supply, demand], axis=1, sort=False)

    offline.plot(
        hourly_plot(
            name=dir, color_dict=color_dict, supply=supply, lines=demand["demand"].to_frame(), demand=demand["phs"].to_frame()),
        filename=os.path.join(plots, "hourly-dispatch.html"),
        auto_open=False,
    )

    # # sorted supply
    # sorted_supply = pd.DataFrame(
    #     {c: supply[c].sort_values().values for c in supply.columns}
    # )
    #
    # plt.figure(figsize=(15,7))
    # ax = sorted_supply.plot(style="-", grid=True, cmap=plt.get_cmap("Set2"))
    # plt.ylabel("Power in MW")
    # plt.xlabel("Hour")
    #
    # lgd = ax.legend(
    #     loc="upper left",
    #     # bbox_to_anchor=(-0.05, -0.45),
    #     # shadow=False,
    #     #frameon=False,
    #     ncol=2,
    # )
    # plt.savefig(
    #     os.path.join(plots, "sorted-supply.pdf"),
    #     bbox_extra_artists=(lgd,),
    #     bbox_inches="tight"
    # )

    # aggregated supply
    fig, ax = plt.subplots(figsize=(15,7))
    aggr = supply.sum() / 1e3
    ax = aggr.plot(kind="bar")
    ax.set_title("Aggregated supply by technology in GWh")
    ax.set_ylabel("Energy in GWh")
    plt.xticks(rotation=45)
    plt.savefig(
        os.path.join(plots, "aggregated_supply.pdf"))
