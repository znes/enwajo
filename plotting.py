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
        title="Hourly supply and demand in for scenario {}".format(name),
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


def create_plots(rdir, config):
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

    supply = pd.read_csv(os.path.join(rdir, "supply.csv"), index_col=[0])

    demand = pd.read_csv(os.path.join(rdir, "demand.csv"), index_col=[0])

    offline.plot(
        hourly_plot(
            name="test",
            color_dict=color_dict,
            supply=supply,
            lines=demand["demand"].to_frame(),
            demand=demand["phs"].to_frame(),
        ),
        filename=os.path.join(plots, "hourly-dispatch.html"),
        auto_open=False,
    )
    return plots
