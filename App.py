import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------------

st.set_page_config(
    page_title="Dashboard METAR SPSO",
    page_icon="🌦️",
    layout="wide"
)

st.title("🌦️ Dashboard Meteorológico METAR - SPSO")
st.markdown("Análisis interactivo de variables meteorológicas")

# -----------------------------------
# CARGA DE DATOS
# -----------------------------------

@st.cache_data
def cargar_datos():
    df = pd.read_csv("metars_SPSO_2025.csv")
    return df

df = cargar_datos()

# -----------------------------------
# MOSTRAR COLUMNAS
# -----------------------------------

st.subheader("📋 Vista previa de datos")

st.dataframe(df.head())

# -----------------------------------
# DETECTAR COLUMNAS NUMÉRICAS
# -----------------------------------

columnas_numericas = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

# -----------------------------------
# SIDEBAR - PANEL PLEGABLE
# -----------------------------------

with st.sidebar:
    st.header("⚙️ Configuración")

    variable = st.selectbox(
        "Selecciona variable meteorológica",
        columnas_numericas
    )

    tipo_grafico = st.selectbox(
        "Tipo de gráfico",
        ["Línea", "Área", "Histograma", "Boxplot"]
    )

    mostrar_estadisticas = st.checkbox(
        "Mostrar estadísticas",
        value=True
    )

# -----------------------------------
# EJE X (TIEMPO)
# -----------------------------------

# Buscar automáticamente una columna de fecha/hora
columna_fecha = None

for col in df.columns:
    if "date" in col.lower() or "time" in col.lower():
        columna_fecha = col
        break

if columna_fecha:
    try:
        df[columna_fecha] = pd.to_datetime(df[columna_fecha])
    except:
        pass

# -----------------------------------
# DASHBOARD PRINCIPAL
# -----------------------------------

st.subheader(f"📈 Tendencia de: {variable}")

if columna_fecha:

    if tipo_grafico == "Línea":
        fig = px.line(
            df,
            x=columna_fecha,
            y=variable,
            title=f"Tendencia de {variable}"
        )

    elif tipo_grafico == "Área":
        fig = px.area(
            df,
            x=columna_fecha,
            y=variable,
            title=f"Área de {variable}"
        )

    elif tipo_grafico == "Histograma":
        fig = px.histogram(
            df,
            x=variable,
            title=f"Distribución de {variable}"
        )

    elif tipo_grafico == "Boxplot":
        fig = px.box(
            df,
            y=variable,
            title=f"Boxplot de {variable}"
        )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No se encontró columna de fecha/hora")

# -----------------------------------
# ESTADÍSTICAS
# -----------------------------------

if mostrar_estadisticas:

    st.subheader("📊 Estadísticas")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Promedio", round(df[variable].mean(), 2))
    col2.metric("Máximo", round(df[variable].max(), 2))
    col3.metric("Mínimo", round(df[variable].min(), 2))
    col4.metric("Desv. Std", round(df[variable].std(), 2))

# -----------------------------------
# MATRIZ DE CORRELACIÓN
# -----------------------------------

st.subheader("🔍 Correlación entre variables")

corr = df[columnas_numericas].corr()

fig_corr = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Mapa de correlación"
)

st.plotly_chart(fig_corr, use_container_width=True)

# -----------------------------------
# DESCARGA DE DATOS
# -----------------------------------

st.subheader("⬇️ Descargar datos")

csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Descargar CSV",
    data=csv,
    file_name="datos_metar.csv",
    mime="text/csv"
)
