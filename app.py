
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

frekuensi = "Seberapa sering Anda menggunakan aplikasi Livin' By Mandiri"

fig = px.bar(
    df[frekuensi].value_counts().reset_index(),
    x="count",
    y=frekuensi,
    orientation="h",
    title="Frekuensi Penggunaan Livin"
)

st.plotly_chart(fig, use_container_width=True)

kendala = "Apa kendala utama yang Anda alami?"

fig = px.bar(
    df[kendala].value_counts().reset_index(),
    x="count",
    y=kendala,
    orientation="h",
    title="Kendala yang Paling Sering Dialami"
)

st.plotly_chart(fig, use_container_width=True)

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

c1,c3,c4 = st.columns(3)
c1.metric("👥 Total Responden", total)
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

st.subheader("📋 Data Responden")
st.dataframe(df,use_container_width=True)

csv=df.to_csv(index=False).encode("utf-8")
st.download_button("⬇ Download Hasil Filter",csv,"hasil_filter.csv","text/csv")


