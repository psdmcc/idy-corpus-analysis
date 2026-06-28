import os

print("===================================")
print("RUNNING IDY COMPUTATIONAL PIPELINE")
print("===================================\n")

steps = [
    "python analysis/compute_dsi.py",
    "python analysis/year_effects.py",
    "python analysis/interaction_model.py",
    "python analysis/consolidate_outputs.py",
]

for s in steps:
    print(f"\n--- Running: {s} ---")
    os.system(s)

print("\n===================================")
print("PIPELINE COMPLETE")
print("===================================")
