import streamlit as st
import pandas as pd
import altair as alt

def generar_graficos_interactivos():
    st.subheader("Generación Interactiva de Gráficos")

    if 'df' not in st.session_state or st.session_state['df'] is None:
        st.info("Por favor, sube un archivo primero para generar gráficos.")
        return

    df = st.session_state['df']
    columnas = df.columns

    # --- Selectores para el usuario ---
    tipos_de_graficos = ["Selecciona un gráfico", "Gráfico de barras", "Gráfico de líneas", "Gráfico de dispersión", "Histograma", "Gráfico de área", "Boxplot", "Gráfico de torta"]
    tipo_de_grafico = st.selectbox("Selecciona el tipo de gráfico:", tipos_de_graficos)

    x_columna = st.selectbox("Selecciona la columna para el eje X:", [""] + list(columnas), key="x")
    y_columna = st.selectbox("Selecciona la columna para el eje Y:", [""] + list(columnas), key="y")

    # --- Generar el gráfico si se han seleccionado los elementos necesarios ---
    if tipo_de_grafico != "Selecciona un gráfico" and x_columna and (y_columna or tipo_de_grafico == "Histograma" or tipo_de_grafico == "Gráfico de torta"):
        try:
            grafico = crear_grafico(df, tipo_de_grafico, x_columna, y_columna)
            st.altair_chart(grafico, use_container_width=True)
        except Exception as e:
            st.error(f"No se pudo generar el gráfico. Error: {e}")
    elif tipo_de_grafico != "Selecciona un gráfico":
        st.warning("Por favor, selecciona las columnas X e Y.")


def crear_grafico(df, tipo_de_grafico, x_columna, y_columna):
    """Crea el gráfico según el tipo seleccionado."""

    if tipo_de_grafico == "Gráfico de barras":
        grafico = alt.Chart(df).mark_bar().encode(
            x=x_columna,
            y=y_columna,
            tooltip=[x_columna, y_columna]
        ).interactive()
    elif tipo_de_grafico == "Gráfico de líneas":
        grafico = alt.Chart(df).mark_line().encode(
            x=x_columna,
            y=y_columna,
            tooltip=[x_columna, y_columna]
        ).interactive()
    elif tipo_de_grafico == "Gráfico de dispersión":
        grafico = alt.Chart(df).mark_circle().encode(
            x=x_columna,
            y=y_columna,
            tooltip=[x_columna, y_columna]
        ).interactive()
    elif tipo_de_grafico == "Histograma":
        grafico = alt.Chart(df).mark_bar().encode(
            x=alt.X(x_columna, bin=True),
            y='count()',
            tooltip=[x_columna, 'count()']
        ).interactive()
    elif tipo_de_grafico == "Gráfico de área":
        grafico = alt.Chart(df).mark_area().encode(
            x=x_columna,
            y=y_columna,
            tooltip=[x_columna, y_columna]
        ).interactive()
    elif tipo_de_grafico == "Boxplot":
        grafico = alt.Chart(df).mark_boxplot().encode(
            x=x_columna,
            y=y_columna,
            tooltip=[x_columna, y_columna]
        ).interactive()
    elif tipo_de_grafico == "Gráfico de torta":
        base = alt.Chart(df).encode(
            theta=alt.Theta(y_columna, stack=True)
        )
        pie = base.mark_arc(outerRadius=120).encode(
            color=alt.Color(x_columna),
            order=alt.Order(x_columna),
            tooltip=[x_columna, y_columna]
        )
        text = base.mark_text(radius=140).encode(
            text=y_columna,
            order=alt.Order(x_columna),
            color=alt.value("black")
        )
        grafico = pie + text
    return grafico