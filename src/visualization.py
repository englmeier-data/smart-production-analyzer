import pandas as pd
import matplotlib.pyplot as plt

# Daten laden
data = pd.read_csv("data/production_data_analyzed.csv")

# ===== Plot 1: Verlauf Spannung =====
plt.figure()
plt.plot(data["spannung"], label="Spannung")
plt.scatter(
    data.index[data["spannung_outlier"]],
    data["spannung"][data["spannung_outlier"]],
    color="red",
    label="Ausreißer"
)
plt.title("Spannungsverlauf mit Ausreißern")
plt.legend()
plt.xlabel("Messpunkt")
plt.ylabel("Spannung")
plt.grid()


plt.axhline(5.5, color="green", linestyle="--", label="USL")
plt.axhline(4.5, color="green", linestyle="--", label="LSL")

# ===== Plot 2: Verlauf Widerstand =====
plt.figure()
plt.plot(data["widerstand"], label="Widerstand")
plt.scatter(
    data.index[data["widerstand_outlier"]],
    data["widerstand"][data["widerstand_outlier"]],
    color="red",
    label="Ausreißer"
)
plt.title("Widerstand mit Ausreißern")
plt.legend()
plt.xlabel("Messpunkt")
plt.ylabel("Widerstand")
plt.grid()

# ===== Plot 3: Histogramm =====
plt.figure()
plt.hist(data["spannung"], bins=20)
plt.title("Verteilung Spannung")

plt.figure()
plt.hist(data["widerstand"], bins=20)
plt.title("Verteilung Widerstand")

plt.show()