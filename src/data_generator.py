import pandas as pd
import numpy as np

np.random.seed(42)

n = 200

data = pd.DataFrame({
    "messzeit": pd.date_range(start="2024-01-01", periods=n, freq="h"),
    "spannung": np.random.normal(5, 0.2, n),
    "widerstand": np.random.normal(100, 5, n)
})

# künstliche Fehler
data.loc[10, "spannung"] = 6
data.loc[50, "widerstand"] = 120

data.to_csv("data/production_data.csv", index=False)

print("CSV erfolgreich erstellt!")