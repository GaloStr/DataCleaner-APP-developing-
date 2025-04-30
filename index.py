import streamlit as st
import pandas as pd
import cleaner
import modify

def cargar_datos():
    """Carga los datos desde un archivo subido y lo guarda en session_state."""
    uploaded_file = st.file_uploader("Sube tu archivo (.csv, .xlsx, .sql)", type=['csv', 'xlsx', 'sql'])
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension == 'csv':
            st.session_state['df'] = pd.read_csv(uploaded_file)
        elif file_extension == 'xlsx':
            st.session_state['df'] = pd.read_excel(uploaded_file)
        elif file_extension == 'sql':
            st.warning("La carga directa de archivos .sql aún no está completamente implementada en este ejemplo.")
            st.session_state['df'] = None
    else:
        st.session_state['df'] = None

def mostrar_tabla():
    """Muestra el DataFrame desde session_state."""
    if 'df' in st.session_state and st.session_state['df'] is not None:
        st.subheader("Tabla de Datos")
        df = st.session_state['df']
        if len(df) > 20:
            st.dataframe(df.head(10))
        else:
            st.dataframe(df)
    else:
        st.info("Por favor, sube un archivo para ver la tabla.")

def descargar_df():
    """Descarga el DataFrame desde session_state."""
    if 'df' in st.session_state and st.session_state['df'] is not None:
        st.download_button(
            label="Descargar DataFrame Limpio como CSV",
            data=st.session_state['df'].to_csv(index=False).encode('utf-8'),
            file_name="dataframe_limpio.csv",
            mime="text/csv",
        )

def main():
    st.title("Herramienta de Análisis y Limpieza de Datos")

    cargar_datos()

    st.sidebar.title("Navegación")
    menu = ["Limpieza de Datos", "Modificación de Tablas / Datos", "Visión de Tabla", "Gráficos"]
    choice = st.sidebar.selectbox("Selecciona una categoría:", menu)

    if choice == "Limpieza de Datos":
        cleaner.limpiar_duplicados_ui()
        cleaner.limpiar_nulos_ui()
    elif choice == "Modificación de Tablas / Datos":
        if 'df' in st.session_state and st.session_state['df'] is not None:
            modify.modificacion_datos_ui()
        else:
            st.info("Por favor, sube un archivo primero.")
    elif choice == "Visión de Tabla":
        mostrar_tabla()
    elif choice == "Gráficos":
        st.subheader("Generación de Gráficos")
        st.info("Funcionalidades de gráficos en desarrollo...")

    if 'df' in st.session_state and st.session_state['df'] is not None:
        st.sidebar.subheader("Descarga")
        descargar_df()

if __name__ == "__main__":
    main()