import plotly.graph_objs as go


def hourly_plot(name, color_dict, lines=[], supply=[], demand=[]):
    """
    """

    # for i in conventionals:
    #     carrier = i.split("-")[0]
    #     group = [c for c in df.columns if carrier in c]
    #     df[i] = df[group].sum(axis=1)
    #     df.drop(group, axis=1, inplace=True)

    # df = df.resample('1D').mean()
    x = supply.index

    # create plot
    layout = go.Layout(
        barmode="stack",
        title="Hourly supply and demand in for scenario {}".format(
            name
        ),
        yaxis=dict(
            title="Energy in MWh",
            titlefont=dict(size=16, color="rgb(107, 107, 107)"),
            tickfont=dict(size=14, color="rgb(107, 107, 107)"),
        ),
    )

    data = []
    for c in demand:
        demand[c] = demand[c] * - 1
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
