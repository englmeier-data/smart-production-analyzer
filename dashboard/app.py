import streamlit as st
import pandas as pd

st.set_page_config(page_title="Production Dashboard", layout="wide")

st.title("📊 Smart Production Analyzer")

# Daten laden
data = pd.read_csv("data/production_data_analyzed.csv")

# ===== Übersicht =====
st.subheader("📈 Überblick")

col1, col2 = st.columns(2)

with col1:
    st.metric("Messpunkte", len(data))

with col2:
    st.metric("Spannung Mittelwert", round(data["spannung"].mean(), 2))


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