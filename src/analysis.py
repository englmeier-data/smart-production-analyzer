import pandas as pd
import numpy as np



def calculate_cpk(series, lower, upper):
    mean = series.mean()
    std = series.std()

    cp = (upper - lower) / (6 * std)
    cpk = min((upper - mean), (mean - lower)) / (3 * std)

    return cp, cpk


def detect_outliers_zscore(series, threshold=3):
    z_scores = (series - series.mean()) / series.std()
    return np.abs(z_scores) > threshold


# Daten laden
data = pd.read_csv("data/production_data.csv")

print("\n=== Statistische Kennwerte ===")
print(data.describe())

# Cp / Cpk berechnen
cp_sp, cpk_sp = calculate_cpk(data["spannung"], 4.5, 5.5)
cp_w, cpk_w = calculate_cpk(data["widerstand"], 90, 110)

print("=== Prozessfähigkeit ===")
print(f"Spannung: Cp={cp_sp:.2f}, Cpk={cpk_sp:.2f}")
print(f"Widerstand: Cp={cp_w:.2f}, Cpk={cpk_w:.2f}")

# Ausreißer erkennen
data["spannung_outlier"] = detect_outliers_zscore(data["spannung"])
data["widerstand_outlier"] = detect_outliers_zscore(data["widerstand"])

print("\n=== Ausreißer ===")
print("Spannung:", data["spannung_outlier"].sum())
print("Widerstand:", data["widerstand_outlier"].sum())

# Optional speichern
data.to_csv("data/production_data_analyzed.csv", index=False)