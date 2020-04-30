import os

import matplotlib.pyplot as plt
import pandas as pd

if not os.path.exists("results"):
    raise Exception("No result directory found to plot results.")

if not os.path.exists("plots"):
    os.makedirs("plots")

supply = pd.read_csv("results/supply.csv", index_col=[0])

# sorted supply
sorted_supply = pd.DataFrame(
    {c: supply[c].sort_values().values for c in supply.columns}
)
plt.figure()
ax = sorted_supply.plot(style="-", grid=True, cmap=plt.get_cmap("coolwarm"))
plt.ylabel("Power in MW")
plt.xlabel("Hour")

lgd = ax.legend(
    loc="upper left",
    # bbox_to_anchor=(-0.05, -0.45),
    # shadow=False,
    #frameon=False,
    ncol=2,
)
plt.savefig(
    "plots/sorted.pdf",
    bbox_extra_artists=(lgd,),
    bbox_inches="tight"
)

# aggregated supply
fig, ax = plt.subplots()
aggr = supply.sum() / 1e6
ax = aggr.plot(kind="bar")
ax.set_title("Aggregated supply by technology in TWh")
ax.set_ylabel("Energy in TWh")
plt.xticks(rotation=45)
plt.savefig("plots/aggregated_supply.pdf")
