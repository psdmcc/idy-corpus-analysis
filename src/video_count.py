import pandas as pd

df = pd.read_csv("dsi_rows.csv")

news = [
    "WION", "India Today", "NDTV", "CNN-News18",
    "Republic World", "Times Now", "Aaj Tak",
    "DD News", "NEWS9 Live", "Times Of India",
    "Mango News", "Oneindia News", "ANI News"
]

government = [
    "Ministry of Ayush",
    "Ministry of Information & Broadcasting",
    "Directorate Ayurved Uttarakhand",
    "Sansad TV"
]

diplomatic = [
    "Indian Diplomacy",
    "Ministry of External Affairs, India"
]

political = [
    "Narendra Modi",
    "Bharatiya Janata Party"
]

print(
    df[df["channel"].isin(news)]
    .shape[0]
)

print(
    df[df["channel"].isin(government)]
    .shape[0]
)

print(
    df[df["channel"].isin(diplomatic)]
    .shape[0]
)

print(
    df[df["channel"].isin(political)]
    .shape[0]
)
