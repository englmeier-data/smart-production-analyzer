import streamlit as st
import pandas as pd


def calculate_cpk(series, lower, upper):
    mean = series.mean()
    std = series.std()

    cp = (upper - lower) / (6 * std)
    cpk = min((upper - mean), (mean - lower)) / (3 * std)

    return cp, cpk

st.set_page_config(page_title="Production Dashboard", layout="wide")

st.title("📊 Smart Production Analyzer")

# Daten laden
data = pd.read_csv("data/production_data_analyzed.csv")

# Grenzwerte (kann später dynamisch gemacht werden)
SPANNUNG_LSL = 4.5
SPANNUNG_USL = 5.5

WIDERSTAND_LSL = 90
WIDERSTAND_USL = 110


cp_sp, cpk_sp = calculate_cpk(data["spannung"], SPANNUNG_LSL, SPANNUNG_USL)
cp_w, cpk_w = calculate_cpk(data["widerstand"], WIDERSTAND_LSL, WIDERSTAND_USL)

# ===== Übersicht =====
st.subheader("📈 Überblick")

col1, col2 = st.columns(2)

with col1:
    st.metric("Messpunkte", len(data))

with col2:
    st.metric("Spannung Mittelwert", round(data["spannung"].mean(), 2))

st.subheader("📏 Prozessfähigkeit")

col3, col4 = st.columns(2)

with col3:
    st.metric("Cp Spannung", f"{cp_sp:.2f}")
    st.metric("Cpk Spannung", f"{cpk_sp:.2f}")

with col4:
    st.metric("Cp Widerstand", f"{cp_w:.2f}")
    st.metric("Cpk Widerstand", f"{cpk_w:.2f}")




# ===== Verlauf =====
st.subheader("📉 Verlauf")

st.line_chart(data["spannung"])
st.line_chart(data["widerstand"])


# ===== Ausreißer =====
st.subheader("🚨 Ausreißer")

spannung_outliers = data[data["spannung_outlier"]]
widerstand_outliers = data[data["widerstand_outlier"]]

st.write("Spannung Ausreißer:", len(spannung_outliers))
st.write(spannung_outliers)

st.write("Widerstand Ausreißer:", len(widerstand_outliers))
st.write(widerstand_outliers)