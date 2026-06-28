import pandas as pd
import matplotlib.pyplot as plt

table = pd.read_csv(
    "data/analysis/year_cluster_table.csv",
    index_col=0
)

plt.figure(figsize=(10,6))
plt.imshow(table, aspect="auto")
plt.colorbar(label="Video count")

plt.xticks(range(len(table.columns)), table.columns)
plt.yticks(range(len(table.index)), table.index)

plt.xlabel("Cluster")
plt.ylabel("Year")
plt.title("IDY Corpus: Cluster Distribution by Year")

plt.tight_layout()
plt.savefig(
    "data/analysis/year_cluster_heatmap.png",
    dpi=300
)

plt.show()
