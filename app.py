import streamlit as st
import pandas as pd

st.title("Dashboard Livin by Mandiri")

survey = pd.read_csv("survey_clean.csv")

gender = st.selectbox(
    "Pilih Gender",
    survey["Jenis Kelamin"].unique()
)

filtered = survey[
    survey["Jenis Kelamin"] == gender
]

st.dataframe(filtered)