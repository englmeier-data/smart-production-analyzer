import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


uploaded_file = st.file_uploader("CSV-Datei hochladen", type=["csv"])


def calculate_cpk(series, lower, upper):
    mean = series.mean()
    std = series.std()

    cp = (upper - lower) / (6 * std)
    cpk = min((upper - mean), (mean - lower)) / (3 * std)

    return cp, cpk


def evaluate_cpk(cpk):
    if cpk < 1:
        return f"❌ kritisch (Cpk = {cpk:.2f})"
    elif cpk < 1.33:
        return f"⚠️ grenzwertig (Cpk = {cpk:.2f})"
    else:
        return f"✅ gut (Cpk = {cpk:.2f})"
    
def detect_outliers_limits(series, lower, upper):
    return (series < lower) | (series > upper)

st.set_page_config(page_title="Production Dashboard", layout="wide")

st.title("📊 Smart Production Analyzer")

# Daten laden nur wenn Datei vorhanden ist, sonst Standarddaten verwenden
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    data = pd.read_csv("data/production_data_analyzed.csv")

st.subheader("📄 Geladene Daten")
st.dataframe(data.head())

# Spalten nur Zeigen  wenn VSV geladen wurde, sonst Fehler anzeigen
required_columns = ["spannung", "widerstand"]
if not all(col in data.columns for col in required_columns):
    st.error("❌ Die CSV muss die Spalten 'spannung' und 'widerstand' enthalten!")
    st.stop()   

st.subheader("⚙️ Grenzwerte einstellen")

col_settings1, col_settings2 = st.columns(2)

with col_settings1:
    SPANNUNG_LSL = st.number_input("Spannung LSL", value=4.5)
    SPANNUNG_USL = st.number_input("Spannung USL", value=5.5)

with col_settings2:
    WIDERSTAND_LSL = st.number_input("Widerstand LSL", value=90.0)
    WIDERSTAND_USL = st.number_input("Widerstand USL", value=110.0)


# Cp/Cpk Berechnung
cp_sp, cpk_sp = calculate_cpk(data["spannung"], SPANNUNG_LSL, SPANNUNG_USL)
cp_w, cpk_w = calculate_cpk(data["widerstand"], WIDERSTAND_LSL, WIDERSTAND_USL)

## Ausreißer berechnens 
data["spannung_outlier"] = detect_outliers_limits(
data["spannung"], SPANNUNG_LSL, SPANNUNG_USL
)

data["widerstand_outlier"] = detect_outliers_limits(
    data["widerstand"], WIDERSTAND_LSL, WIDERSTAND_USL
)


# ===== Übersicht =====
st.subheader("📈 Überblick")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Messpunkte", len(data))

with col2:
    st.metric("Spannung Mittelwert", round(data["spannung"].mean(), 2))

with col3:
    st.metric("Spannung StdAbw", round(data["spannung"].std(), 2))

with col4:
    st.metric("Widerstand Mittelwert", round(data["widerstand"].mean(), 2))

with col5:
    st.metric("Widerstand StdAbw", round(data["widerstand"].std(), 2))

# ===== Verlauf =====
st.subheader("📉 Verlauf")

fig, ax = plt.subplots(figsize=(4.5, 2.5))


# ##################### DIAGRAMME #####################

col_plot1, col_plot2 = st.columns([1, 1])

# ================== Spannung ==================
with col_plot1:
    fig1, ax1 = plt.subplots(figsize=(4.5, 2.5))

    ax1.plot(data["spannung"], label="Spannung", linewidth=1, color="blue")

    ax1.axhline(SPANNUNG_LSL, linestyle="--", linewidth=1, color="darkred", label="LSL")
    ax1.axhline(SPANNUNG_USL, linestyle="--", linewidth=1, color="darkred", label="USL")
    outliers_sp = data["spannung_outlier"]
    
    ax1.scatter(
        data.index[outliers_sp],
        data["spannung"][outliers_sp],
        color="red",
        marker="x",
        s=25,
        label="Ausreißer"
    )

    ax1.set_title("Spannung")
    ax1.set_xlabel("Messpunkt")
    ax1.set_ylabel("Spannung")
    ax1.legend(fontsize=8, loc="upper right")
    ax1.grid(True, linestyle=":", linewidth=0.5)
    
    st.pyplot(fig1)

# ================== Widerstand ==================
with col_plot2:
    fig2, ax2 = plt.subplots(figsize=(4.5, 2.5))

    ax2.plot(data["widerstand"], label="Widerstand", linewidth=1, color="blue")
    
    ax2.axhline(WIDERSTAND_LSL, linestyle="--", linewidth=1, color="darkred", label="LSL Widerstand")
    ax2.axhline(WIDERSTAND_USL, linestyle="--", linewidth=1, color="darkred", label="USL Widerstand")
  
    outliers_w = data["widerstand_outlier"]
    
    ax2.scatter(
        data.index[outliers_w],
        data["widerstand"][outliers_w],
        color="red",
        marker="x",
        s=25,
        label="Ausreißer"
    )

    ax2.set_title("Widerstand")
    ax2.set_xlabel("Messpunkt")
    ax2.set_ylabel("Widerstand")
    ax2.legend(fontsize=8, loc="upper right")
    ax2.grid(True, linestyle=":", linewidth=0.5)

    st.pyplot(fig2)
    
# ===== Ausreißer =====
#st.subheader("🚨 Ausreißer")

spannung_outliers = data[data["spannung_outlier"]]
widerstand_outliers = data[data["widerstand_outlier"]]

st.write("Spannung Ausreißer:", len(spannung_outliers))
st.write(spannung_outliers)

st.write("Widerstand Ausreißer:", len(widerstand_outliers))
st.write(widerstand_outliers)