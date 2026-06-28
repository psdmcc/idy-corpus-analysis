import pandas as pd
import matplotlib.pyplot as plt

table = pd.read_csv(
    "data/analysis/year_cluster_table.csv",
    index_col=0
)

pct = table.div(table.sum(axis=1), axis=0) * 100

plt.figure(figsize=(12,6))
plt.imshow(pct, aspect="auto")

plt.colorbar(label="% of yearly corpus")

plt.xticks(
    range(len(pct.columns)),
    pct.columns
)

plt.yticks(
    range(len(pct.index)),
    pct.index
)

plt.xlabel("Cluster")
plt.ylabel("Year")
plt.title("IDY Discourse Clusters by Year")

plt.tight_layout()
plt.show()
