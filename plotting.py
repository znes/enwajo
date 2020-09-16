import os

import matplotlib.pyplot as plt
from matplotlib import colors

import pandas as pd
import plotly.offline as offline
import plotly.graph_objs as go


def hourly_plot(name, color_dict, lines=[], supply=[], demand=[]):
    """
    """
    x = supply.index

    # create plot
    layout = go.Layout(
        barmode="stack",
        title="Hourly supply and demand for {}".format(name),
        yaxis=dict(
            title="Energy in MWh",
            titlefont=dict(size=16, color="rgb(107, 107, 107)"),
            tickfont=dict(size=14, color="rgb(107, 107, 107)"),
        ),
    )

    data = []
    for c in demand:
        demand[c] = demand[c] * -1
        data.append(
            go.Scatter(
                x=x,
                y=demand[c].clip(upper=0),
                name=name,
                stackgroup="negative",
                line=dict(width=0, color=color_dict.get(c, "black")),
                showlegend=False,
            )
        )

    for c in lines:
        # append load
        data.append(
            go.Scatter(
                x=x,
                y=lines[c],
                name=c,
                line=dict(width=3, color=color_dict.get(c)),
            )
        )

    for c in supply:
        if "excess" in c:
            pass
        else:
            data.append(
                go.Scatter(
                    x=x,
                    fillcolor=color_dict.get(c, "black"),
                    y=supply[c],
                    name=c,
                    stackgroup="positive",
                    line=dict(width=0, color=color_dict.get(c, "black")),
                )
            )

    return {"data": data, "layout": layout}


def create_plots(rdir, config, supply, demand):
    """
    """
    if not os.path.exists(rdir):
        raise Exception("No result directory found to plot results.")

    # convert color names to hex for matplotlib
    color_dict = {
        name: colors.to_hex(color) for name, color in config["colors"].items()
    }

    plots = os.path.join(rdir, "plots")

    if not os.path.exists(plots):
        os.makedirs(plots)

    if "phs" in demand.columns:
        phs = demand["phs"].to_frame()
    else:
        phs = pd.DataFrame(index=demand.index)
    offline.plot(
        hourly_plot(
            name=rdir.split("/")[1],
            color_dict=color_dict,
            supply=supply,
            lines=demand["demand"].to_frame(),
            demand=phs,
        ),
        filename=os.path.join(plots, "hourly-dispatch.html"),
        auto_open=False,
    )

    # pie chart for supply
    summary = supply.sum() / 1e6
    summary.name = "Energy"

    ax = summary.plot(
        kind="pie",
        colors=[color_dict.get(c, "black") for c in summary.index],
        title=rdir.split("/")[1])
    plt.savefig(os.path.join(rdir, "plots", "supply-share.pdf"), bbox_inches="tight")
    plt.close()

    bardata = pd.concat([demand.sum() * -1, supply.sum()], sort=False).divide(1e6)
    ax = bardata.plot(kind="barh", title=rdir.split("/")[1])
    ax.set_ylabel("Technologies")
    ax.set_xlabel("Energy in TWh")
    plt.savefig(os.path.join(rdir, "plots", "summary-barplot.pdf"), bbox_inches="tight")
    #


    return plots

if __name__ == "__main__":
    import sys
    import toml

    if len(sys.argv) < 2:
        print("ERROR: Please provide results directory.")
    else:
        with open(os.path.join(sys.argv[1], "config.toml")) as config_data:
            config = toml.load(config_data)
        create_plots(os.path.join(sys.argv[1], "output"), config)
