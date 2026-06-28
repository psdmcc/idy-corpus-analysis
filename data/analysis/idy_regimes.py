import pandas as pd

regimes = pd.DataFrame({

    "year": [

        2015,
        2016,
        2017,
        2018,
        2019,
        2020,
        2021,
        2022,
        2023,
        2024,
        2025,
        2026

    ],

    "regime": [

        "global_legitimation",
        "global_legitimation",
        "institutionalisation",
        "wellness_expansion",
        "wellness_expansion",
        "public_health",
        "resilience",
        "recovery",
        "post_pandemic_recovery",
        "self_society",
        "one_earth_one_health",
        "healthy_ageing"

    ]

})

regimes.to_csv(
    "data/analysis/idy_regimes.csv",
    index=False
)

print(regimes)
