
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Livin by Mandiri", layout="wide")


st.markdown("""
<style>
.main {background-color:#f7fbff;}
h1,h2,h3 {color:#0A5EB0;}
div[data-testid="stMetric"]{
    background:#e8f4ff;
    border-radius:12px;
    padding:12px;
    border:1px solid #b8dfff;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load():
    return pd.read_csv("survey_clean.csv")

survey = load()

col1, col2 = st.columns([1,5])

with col1:
    st.image("logo.png", width=100)

with col2:
    st.title("Dashboard Livin' by Mandiri")
    st.caption("Analisis Kepuasan Pengguna")
st.sidebar.header("🔍 Filter")

df = survey.copy()

if "Jenis Kelamin" in df.columns:
    g = st.sidebar.multiselect(
        "Jenis Kelamin",
        sorted(df["Jenis Kelamin"].dropna().unique()),
        default=list(sorted(df["Jenis Kelamin"].dropna().unique()))
    )
    df = df[df["Jenis Kelamin"].isin(g)]

usia_col = next((c for c in df.columns if "Usia" in c), None)
if usia_col:
    usia = st.sidebar.multiselect(
        "Usia",
        sorted(df[usia_col].dropna().astype(str).unique()),
        default=list(sorted(df[usia_col].dropna().astype(str).unique()))
    )
    df = df[df[usia_col].astype(str).isin(usia)]

status_col = next((c for c in df.columns if "Status" in c), None)
if status_col:
    stat = st.sidebar.multiselect(
        "Status Responden",
        sorted(df[status_col].dropna().astype(str).unique()),
        default=list(sorted(df[status_col].dropna().astype(str).unique()))
    )
    df = df[df[status_col].astype(str).isin(stat)]

total = len(df)

rating_col = next((c for c in df.columns if "Rating" in c or "rating" in c), None)
avg_rating = "-"
if rating_col:
    try:
        avg_rating = round(pd.to_numeric(df[rating_col], errors="coerce").mean(),2)
    except:
        pass

c1,c2,c3,c4 = st.columns(4)
c1.metric("👥 Total Responden", total)
c2.metric("⭐ Rata-rata Rating", avg_rating)
c3.metric("📋 Jumlah Kolom", len(df.columns))
c4.metric("📊 Data Tersaring", len(df))

col1,col2 = st.columns(2)

with col1:
    if "Jenis Kelamin" in df.columns:
        fig=px.pie(df,names="Jenis Kelamin",title="Distribusi Gender",
                   color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig,use_container_width=True)

with col2:
    if status_col:
        fig=px.bar(df[status_col].value_counts().reset_index(),
                   x="count",y=status_col,orientation="h",
                   title="Status Responden")
        st.plotly_chart(fig,use_container_width=True)

col3,col4=st.columns(2)

with col3:
    if usia_col:
        fig=px.histogram(df,x=usia_col,title="Distribusi Usia",
                         color_discrete_sequence=["#0A5EB0"])
        st.plotly_chart(fig,use_container_width=True)

with col4:
    if rating_col:
        fig=px.histogram(df,x=rating_col,title="Distribusi Rating",
                         color_discrete_sequence=["#FFD43B"])
        st.plotly_chart(fig,use_container_width=True)

st.subheader("📋 Data Responden")
st.dataframe(df,use_container_width=True)

csv=df.to_csv(index=False).encode("utf-8")
st.download_button("⬇ Download Hasil Filter",csv,"hasil_filter.csv","text/csv")

st.markdown("---")
st.success("Dashboard Livin' by Mandiri selesai dibuat 🚀")
