## Importálások
# pandas: adatok tisztításához használt csomag
import pandas as pd
# matplotlib: diagramok, ábrák készítése, "plotolás"
import matplotlib.pyplot as plt
# numpy: numerikus műveletek a különböző adatokkal -> lineáris regresszióhoz kell
import numpy as np

######################################################################

## Adatok tisztítása

# Beolvasás: az első sort átugorjuk (csak címsor, nem header)
df = pd.read_csv("stadat-ido0003-10.1.1.3-en.csv", sep=";", skiprows=1)

# Oszlopnevek tisztítása: fölösleges whitespace eltávolítása
df.columns = df.columns.str.strip()

# Automatikus normalizálás (szóközök helyett alulvonás stb.)
df.columns = (
    df.columns
      .str.replace(" ", "_", regex=False)
      .str.replace("–", "-", regex=False)   # hosszú kötőjel normalizálása
      .str.replace("/", "_", regex=False)   # évek miatt
)

# Eredmény ellenőrzése
print(df.head())
print(df.describe())

# Fájlba írjuk a megtisztított adatstruktúrát
df.to_csv("cleaned_data.csv", index=False, sep=';')
print("Az adatok kiírásra kerültek a new_data.csv fájlba.")

######################################################################

## Leíró statisztika készítése

# Biztos, ami biztos: Activity marad szöveg, a többi numerikus
num_cols = [c for c in df.columns if c != "Activity"]
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce")

# Csak a numerikus rész külön (könnyebb vele dolgozni)
num_df = df[num_cols]

# Leíró statisztika soronként (minden Activity-re)
stats_df = pd.DataFrame({
    "Activity": df["Activity"],
    "count":   num_df.count(axis=1),
    "mean":    num_df.mean(axis=1),
    "median":  num_df.median(axis=1),
    "std":     num_df.std(axis=1),
    "min":     num_df.min(axis=1),
    "25%":     num_df.quantile(0.25, axis=1),
    "75%":     num_df.quantile(0.75, axis=1),
    "max":     num_df.max(axis=1),
})

print("Leíró statisztikai elemzés:")

# Eredmény kiírása
print(stats_df.head())

# Mentés új CSV-be
stats_df.to_csv("activity_descriptive_stats.csv", sep=";", index=False)
print("Leíró statisztika elkészült: activity_descriptive_stats.csv")

######################################################################

## Vonaldiagram: mean, median, min, max értékek aktivitásonként

# méretek beállítása
plt.figure(figsize=(12, 6))
# különböző megjelenítendő adatok beállítása, cimkézése
plt.plot(stats_df["Activity"], stats_df["mean"], marker="o", label="Átlag (mean)")
plt.plot(stats_df["Activity"], stats_df["median"], marker="o", label="Medián")
plt.plot(stats_df["Activity"], stats_df["min"], marker="o", label="Minimum")
plt.plot(stats_df["Activity"], stats_df["max"], marker="o", label="Maximum")
# szöveg elforgatása, hogy kiférjen
plt.xticks(rotation=90)
# y tengely cimke
plt.ylabel("perc / fő / nap")
# cím
plt.title("Leíró statisztikák – Vonaldiagram")
plt.legend()
plt.tight_layout()
# diagram megjelenítése
plt.show()

######################################################################

##  Oszlopdiagram: átlagos értékek (mean)

# méretek beállítása
plt.figure(figsize=(12, 6))
# oszlopokhoz tartozó adat megadása
plt.bar(stats_df["Activity"], stats_df["mean"])
# szöveg elforgatása, hogy olvasható legyen
plt.xticks(rotation=90)
# y tengely cimke
plt.ylabel("perc / fő / nap")
# cím
plt.title("Átlagos időráfordítás tevékenységenként (mean)")
plt.tight_layout()
# diagram megjelenítése
plt.show()

######################################################################

## Vonaldiagram korcsoportonként

# Az elemzéshez és lineáris regresszióhoz szükséges hosszú formára alakítás
num_cols = df.columns[df.columns != "Activity"]

long_df = df.melt(
    id_vars="Activity",
    value_vars=num_cols,
    var_name="col",
    value_name="minutes"
)

# Oszlopnevek szétbontása: age_group, sex, év
pattern = r"(?P<age>\d{2}-\d{2}_year-old)_(?P<sex>males|females|total)_(?P<y1>\d{4})_(?P<y2>\d{4})"
parts = long_df["col"].str.extract(pattern)

long_df = pd.concat([long_df, parts], axis=1)

# Középső év
long_df["year"] = (long_df["y1"].astype(float) + long_df["y2"].astype(float)) / 2
long_df["minutes"] = pd.to_numeric(long_df["minutes"], errors="coerce")

# Egy Activity kiválasztása
activity = "Income producing activity"

subset = long_df[long_df["Activity"] == activity]

# A diagram elkészítése
# méretek beállítása
plt.figure(figsize=(12, 6))

# diagram kirajzolása a megfelelő korcsoportonkénti adatokkal
for age_group, group in subset.groupby("age"):
    group_sorted = group[group["sex"] == "total"].sort_values("year")
    plt.plot(group_sorted["year"], group_sorted["minutes"], marker="o", label=age_group)

# cím
plt.title(f"{activity} – korcsoportonként")
# x tengely cimke
plt.xlabel("Év (időszak közepe)")
# y tengely cimke
plt.ylabel("perc / fő / nap")
# jelmagyarázat
plt.legend(title="Korcsoport")
# négyzetrács berajzolása
plt.grid(True)
plt.tight_layout()
# diagram megrajzolása
plt.show()

######################################################################

## Lineáris regresszió
# adatok előkészítése
sub = long_df[
    (long_df["Activity"] == activity) &
    (long_df["sex"] == "total")           # csak total értékek
].sort_values("year")

x = sub["year"].values
y = sub["minutes"].values

# Lineáris regresszió kiszámítása (y = a*x + b)
a, b = np.polyfit(x, y, 1)
y_pred = a * x + b

# Eredmény kiírása
print(f"Lineáris regresszió eredménye a '{activity}' aktivitásra:")
print(f"  Meredekség (slope): {a:.3f} perc/év")
print(f"  Metszéspont (intercept): {b:.3f}")
print(f"  Változás összesen (1986→2025): {y[-1] - y[0]:.1f} perc")

# Ábra rajzolása
plt.figure(figsize=(10, 6), )
plt.scatter(x, y, label="Megfigyelt értékek")
plt.plot(x, y_pred, label="Lineáris regresszió", linestyle="--")
# cím
plt.title(f"{activity} – lineáris regresszió\n(total érték)")
# x tengely cimke
plt.xlabel("Év (időszak közepe)")
# y tengely cimke
plt.ylabel("perc / fő / nap")
# négyzetrács rajzolása
plt.grid(True)
plt.legend()
plt.tight_layout()
# diagram megjelenítése
plt.show()

print("Program vége.")
## VÉGE ##