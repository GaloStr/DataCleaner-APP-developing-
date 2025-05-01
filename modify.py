import streamlit as st
import pandas as pd

def _renombrar_columna(columna_a_renombrar, nuevo_nombre):
    """Función callback para renombrar columna."""
    if columna_a_renombrar and nuevo_nombre:
        try:
            st.session_state['df'] = st.session_state['df'].rename(
                columns={columna_a_renombrar: nuevo_nombre}
            )
            st.success(f"Columna '{columna_a_renombrar}' renombrada a '{nuevo_nombre}'.")
            # Limpiar los inputs después del éxito
            st.session_state["selectbox_renombrar_modify"] = ""
            st.session_state["input_nuevo_nombre_modify"] = ""
        except KeyError:
            st.error(f"Error: La columna '{columna_a_renombrar}' no existe.")
    else:
        st.warning("Por favor, selecciona una columna y proporciona un nuevo nombre.")


def _cambiar_tipo_columna(columna_a_cambiar_tipo, nuevo_tipo):
    """Función callback para cambiar el tipo de columna."""
    if columna_a_cambiar_tipo and nuevo_tipo:
        try:
            df_temp = st.session_state['df'].copy()
            if nuevo_tipo == "datetime64[ns]":
                df_temp[columna_a_cambiar_tipo] = pd.to_datetime(
                    df_temp[columna_a_cambiar_tipo], errors='coerce'
                )
            elif nuevo_tipo == "boolean":
                df_temp[columna_a_cambiar_tipo] = df_temp[columna_a_cambiar_tipo].map(
                    lambda x: str(x).lower() in ['true', '1', 't', 'y', 'yes'] if pd.notna(x) else x
                ).astype('boolean')
            elif nuevo_tipo in ['int', 'float']:
                df_temp[columna_a_cambiar_tipo] = pd.to_numeric(
                    df_temp[columna_a_cambiar_tipo], errors='coerce'
                )
                if nuevo_tipo == 'int':
                    df_temp[columna_a_cambiar_tipo] = df_temp[columna_a_cambiar_tipo].astype('Int64')
            else:
                df_temp[columna_a_cambiar_tipo] = df_temp[columna_a_cambiar_tipo].astype(
                    nuevo_tipo, errors='ignore'
                )
            st.session_state['df'] = df_temp
            st.success(f"Columna '{columna_a_cambiar_tipo}' convertida a '{nuevo_tipo}'.")
            # Limpiar los inputs después del éxito
            st.session_state["selectbox_tipo_modify"] = ""
            st.session_state["selectbox_nuevo_tipo_modify"] = ""
        except KeyError:
            st.error(f"Error: La columna '{columna_a_cambiar_tipo}' no existe.")
        except ValueError as e:
            st.error(f"Error al convertir: {e}")
    else:
        st.warning("Por favor, selecciona columna y tipo.")


def _reemplazar_valores(columna_a_reemplazar_valor, valor_a_buscar, nuevo_valor):
    """Función callback para reemplazar valores."""
    if columna_a_reemplazar_valor and valor_a_buscar and nuevo_valor:
        try:
            df_temp_reemplazar = st.session_state['df'].copy()
            df_temp_reemplazar[columna_a_reemplazar_valor] = df_temp_reemplazar[
                columna_a_reemplazar_valor
            ].replace(valor_a_buscar, nuevo_valor)
            st.session_state['df'] = df_temp_reemplazar
            st.success(f"Valores en columna '{columna_a_reemplazar_valor}' reemplazados.")
            # Limpiar los inputs después del éxito
            st.session_state["selectbox_reemplazar_modify"] = ""
            st.session_state["input_valor_buscar_modify"] = ""
            st.session_state["input_nuevo_valor_modify"] = ""
        except KeyError:
            st.error(f"Error: La columna '{columna_a_reemplazar_valor}' no existe.")
    else:
        st.warning("Por favor, completa todos los campos.")


def modificacion_datos_ui():
    st.subheader("Modificación de Tablas / Datos")
    # Verificar si el DataFrame existe en el estado de la sesión
    if 'df' not in st.session_state or st.session_state['df'] is None:
        st.info("Por favor, sube un archivo primero.")
        return

    st.subheader("Tabla (Actualizada en tiempo real)")
    # Mostrar siempre el DataFrame principal
    df_display = st.session_state['df'].copy()
    if len(df_display) > 20:
        st.write("Mostrando las primeras 10 filas (la tabla es grande):")
        st.dataframe(df_display.head(10))
    else:
        st.dataframe(df_display)

    st.info("Nota: Los cambios se aplican directamente y no se pueden deshacer fácilmente.", icon="⚠️")

    st.subheader("Opciones de Modificación")

    # --- Renombrar Columna ---
    st.subheader("Renombrar Columna")
    columna_a_renombrar_key = "selectbox_renombrar_modify"
    nuevo_nombre_key = "input_nuevo_nombre_modify"
    boton_renombrar_key = "boton_renombrar_modify"

    # Inicializar el estado de los widgets si no existen
    if columna_a_renombrar_key not in st.session_state:
        st.session_state[columna_a_renombrar_key] = ""
    if nuevo_nombre_key not in st.session_state:
        st.session_state[nuevo_nombre_key] = ""

    columnas_actuales = list(st.session_state['df'].columns)
    columna_a_renombrar = st.selectbox(
        "Selecciona la columna a renombrar:",
        [""] + columnas_actuales,
        key=columna_a_renombrar_key,
        index=columnas_actuales.index(st.session_state[columna_a_renombrar_key]) if st.session_state[columna_a_renombrar_key] in columnas_actuales else 0
    )
    nuevo_nombre = st.text_input(
        "Nuevo nombre de la columna:",
        key=nuevo_nombre_key,
        value=st.session_state[nuevo_nombre_key]
    )
    st.button(
        "Renombrar",
        key=boton_renombrar_key,
        on_click=_renombrar_columna,
        args=(columna_a_renombrar, nuevo_nombre)
    )

    # --- Cambiar Tipo de Datos ---
    st.subheader("Cambiar Tipo de Datos")
    columna_tipo_key = "selectbox_tipo_modify"
    nuevo_tipo_key = "selectbox_nuevo_tipo_modify"
    boton_cambiar_tipo_key = "boton_cambiar_tipo_modify"

    # Inicializar el estado de los widgets si no existen
    if columna_tipo_key not in st.session_state:
        st.session_state[columna_tipo_key] = ""
    if nuevo_tipo_key not in st.session_state:
        st.session_state[nuevo_tipo_key] = ""

    columnas_actuales_tipo = list(st.session_state['df'].columns)
    columna_a_cambiar_tipo = st.selectbox(
        "Selecciona la columna a cambiar:",
        [""] + columnas_actuales_tipo,
        key=columna_tipo_key,
        index=columnas_actuales_tipo.index(st.session_state[columna_tipo_key]) if st.session_state[columna_tipo_key] in columnas_actuales_tipo else 0
    )
    nuevo_tipo = st.selectbox(
        "Selecciona el nuevo tipo:",
        ["", "int", "float", "str", "datetime64[ns]", "boolean"],
        key=nuevo_tipo_key,
        index=0
    )
    st.button(
        "Cambiar Tipo",
        key=boton_cambiar_tipo_key,
        on_click=_cambiar_tipo_columna,
        args=(columna_a_cambiar_tipo, nuevo_tipo)
    )

    # --- Reemplazar Valores ---
    st.subheader("Reemplazar Valores")
    columna_reemplazar_key = "selectbox_reemplazar_modify"
    valor_a_buscar_key = "input_valor_buscar_modify"
    nuevo_valor_key = "input_nuevo_valor_modify"
    boton_reemplazar_key = "boton_reemplazar_modify"

    # Inicializar el estado de los widgets si no existen
    if columna_reemplazar_key not in st.session_state:
        st.session_state[columna_reemplazar_key] = ""
    if valor_a_buscar_key not in st.session_state:
        st.session_state[valor_a_buscar_key] = ""
    if nuevo_valor_key not in st.session_state:
        st.session_state[nuevo_valor_key] = ""

    columnas_actuales_reemplazar = list(st.session_state['df'].columns)
    columna_a_reemplazar_valor = st.selectbox(
        "Selecciona la columna:",
        [""] + columnas_actuales_reemplazar,
        key=columna_reemplazar_key,
        index=columnas_actuales_reemplazar.index(st.session_state[columna_reemplazar_key]) if st.session_state[columna_reemplazar_key] in columnas_actuales_reemplazar else 0
    )
    valor_a_buscar = st.text_input(
        "Valor a buscar:",
        key=valor_a_buscar_key,
        value=st.session_state[valor_a_buscar_key]
    )
    nuevo_valor = st.text_input(
        "Nuevo valor:",
        key=nuevo_valor_key,
        value=st.session_state[nuevo_valor_key]
    )
    st.button(
        "Reemplazar",
        key=boton_reemplazar_key,
        on_click=_reemplazar_valores,
        args=(columna_a_reemplazar_valor, valor_a_buscar, nuevo_valor)
    )