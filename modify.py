import streamlit as st
import pandas as pd

def modificacion_datos_ui():
    st.subheader("Modificación de Tablas / Datos")
    # Verificar si el DataFrame existe en el estado de la sesión
    if 'df' in st.session_state and st.session_state['df'] is not None:

        st.subheader("Tabla (Actualizada en tiempo real)")
        # Mostrar siempre el DataFrame principal
        df_display = st.session_state['df'] # Usar variable local para mostrar
        if len(df_display) > 20:
            st.write("Mostrando las primeras 10 filas (la tabla es grande):")
            st.dataframe(df_display.head(10))
        else:
            st.dataframe(df_display)

        st.info("Nota: Los cambios se aplican directamente y no se pueden deshacer fácilmente.", icon="⚠️")

        st.subheader("Opciones de Modificación")

        # --- Modificar nombre de columna ---
        st.subheader("Renombrar Columna")
        columna_a_renombrar_key = "selectbox_renombrar_modify"
        nuevo_nombre_key = "input_nuevo_nombre_modify"
        boton_renombrar_key = "boton_renombrar_modify"

        # --- Control para limpiar el input 'nuevo_nombre' después de éxito ---
        valor_inicial_nuevo_nombre = ""
        # Si el flag 'rename_successful' es True (viene del rerun anterior)...
        if st.session_state.get('rename_successful', False):
            valor_inicial_nuevo_nombre = "" # ... el valor inicial será vacío.
            st.session_state['rename_successful'] = False # ... y reseteamos el flag.
        else:
            # Si no, mantenemos el valor que tenía (Streamlit lo guarda internamente)
             valor_inicial_nuevo_nombre = st.session_state.get(nuevo_nombre_key, "")

        # --- Widgets Renombrar ---
        columnas_actuales = list(st.session_state['df'].columns)
        columna_a_renombrar = st.selectbox(
            "Selecciona la columna a renombrar:",
            [""] + columnas_actuales,
            key=columna_a_renombrar_key
        )
        # Pasamos el valor inicial controlado al widget
        nuevo_nombre_input = st.text_input(
            "Nuevo nombre de la columna:",
            value=valor_inicial_nuevo_nombre, # <--- Usar el valor controlado
            key=nuevo_nombre_key
        )

        if st.button("Renombrar", key=boton_renombrar_key):
            # Leemos el valor actual que el usuario introdujo en el input
            nuevo_nombre_val = nuevo_nombre_input
            if columna_a_renombrar and nuevo_nombre_val:
                if columna_a_renombrar in st.session_state['df'].columns:
                    try:
                        st.session_state['df'] = st.session_state['df'].rename(columns={columna_a_renombrar: nuevo_nombre_val})
                        st.success(f"La columna '{columna_a_renombrar}' se renombró a '{nuevo_nombre_val}'.")
                        # --- Marcar para limpiar en el próximo rerun ---
                        st.session_state['rename_successful'] = True
                        st.rerun() # Forzar rerun para actualizar todo
                    except Exception as e:
                        st.error(f"Error al renombrar: {e}")
                        st.session_state['rename_successful'] = False # Asegurar reset del flag en error
                else:
                    st.warning(f"La columna '{columna_a_renombrar}' ya no existe. Refresca la selección.")
                    st.session_state['rename_successful'] = False
            else:
                st.warning("Por favor, selecciona una columna y proporciona un nuevo nombre.")
                st.session_state['rename_successful'] = False


        # --- Modificar tipo de datos de columna ---
        st.subheader("Cambiar Tipo de Datos de Columna")
        columna_tipo_key = "selectbox_tipo_modify"
        nuevo_tipo_key = "selectbox_nuevo_tipo_modify"
        boton_cambiar_tipo_key = "boton_cambiar_tipo_modify"

        # (La lógica de limpiar no aplica a selectbox usualmente, se mantiene simple)
        columnas_actuales_tipo = list(st.session_state['df'].columns)
        columna_tipo = st.selectbox(
            "Selecciona la columna a modificar:",
            [""] + columnas_actuales_tipo,
            key=columna_tipo_key
        )
        nuevo_tipo = st.selectbox(
            "Selecciona el nuevo tipo de datos:",
            ["", "int", "float", "str", "datetime64[ns]", "boolean"],
            key=nuevo_tipo_key
        )

        if st.button("Cambiar Tipo", key=boton_cambiar_tipo_key):
            if columna_tipo and nuevo_tipo:
                if columna_tipo in st.session_state['df'].columns:
                    try:
                        df_temp = st.session_state['df']
                        if nuevo_tipo == "datetime64[ns]":
                            df_temp[columna_tipo] = pd.to_datetime(df_temp[columna_tipo], errors='coerce')
                        elif nuevo_tipo == "boolean":
                             df_temp[columna_tipo] = df_temp[columna_tipo].map(
                                 lambda x: str(x).lower() in ['true', '1', 't', 'y', 'yes'] if pd.notna(x) else x
                             ).astype('boolean')
                        else:
                             # Convertir a numérico requiere manejo de errores específico
                             if nuevo_tipo in ['int', 'float']:
                                 df_temp[columna_tipo] = pd.to_numeric(df_temp[columna_tipo], errors='coerce')
                                 # Si se pide int, intentar convertir float resultante a int nullable
                                 if nuevo_tipo == 'int':
                                     # Usar Int64 (nullable) para evitar error con NaN
                                     df_temp[columna_tipo] = df_temp[columna_tipo].astype('Int64')
                             else: # Para 'str' u otros
                                 df_temp[columna_tipo] = df_temp[columna_tipo].astype(nuevo_tipo, errors='ignore')

                        st.session_state['df'] = df_temp
                        st.success(f"El tipo de datos de la columna '{columna_tipo}' se intentó cambiar a '{nuevo_tipo}'. Verifica la tabla.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"No se pudo cambiar el tipo de datos de '{columna_tipo}' a '{nuevo_tipo}'. Error: {e}")
                else:
                     st.warning(f"La columna '{columna_tipo}' ya no existe. Refresca la selección.")
            else:
                st.warning("Por favor, selecciona una columna y un nuevo tipo de datos.")


        # --- Modificar valores (ejemplo básico de reemplazo) ---
        st.subheader("Reemplazar Valores en Columna")
        columna_valor_key = "selectbox_valor_modify"
        valor_a_buscar_key = "input_valor_buscar_modify"
        nuevo_valor_key = "input_nuevo_valor_modify"
        boton_reemplazar_valor_key = "boton_reemplazar_valor_modify"

        # --- Control para limpiar inputs después de éxito ---
        valor_inicial_buscar = ""
        valor_inicial_nuevo = ""
        if st.session_state.get('replace_successful', False):
            valor_inicial_buscar = ""
            valor_inicial_nuevo = ""
            st.session_state['replace_successful'] = False # Resetea el flag
        else:
            valor_inicial_buscar = st.session_state.get(valor_a_buscar_key, "")
            valor_inicial_nuevo = st.session_state.get(nuevo_valor_key, "")

        # --- Widgets Reemplazar ---
        columnas_actuales_valor = list(st.session_state['df'].columns)
        columna_valor = st.selectbox(
            "Selecciona la columna para reemplazar valores:",
            [""] + columnas_actuales_valor,
            key=columna_valor_key
        )
        valor_a_buscar_input = st.text_input(
            "Valor a buscar:",
            value=valor_inicial_buscar,
            key=valor_a_buscar_key
        )
        nuevo_valor_input = st.text_input(
            "Nuevo valor:",
            value=valor_inicial_nuevo,
            key=nuevo_valor_key
        )

        if st.button("Reemplazar Valor", key=boton_reemplazar_valor_key):
            # Leer valores actuales de los inputs
            valor_a_buscar_val = valor_a_buscar_input
            nuevo_valor_val = nuevo_valor_input

            if columna_valor and valor_a_buscar_val != "" and nuevo_valor_val != "":
                if columna_valor in st.session_state['df'].columns:
                    try:
                        dtype_col = st.session_state['df'][columna_valor].dtype
                        valor_a_buscar_typed = valor_a_buscar_val
                        nuevo_valor_typed = nuevo_valor_val

                        # Intentar convertir a tipo de columna (manejo básico)
                        try:
                           if pd.api.types.is_numeric_dtype(dtype_col):
                               valor_a_buscar_typed = pd.to_numeric(valor_a_buscar_val)
                               nuevo_valor_typed = pd.to_numeric(nuevo_valor_val)
                           elif pd.api.types.is_datetime64_any_dtype(dtype_col):
                               valor_a_buscar_typed = pd.to_datetime(valor_a_buscar_val)
                               nuevo_valor_typed = pd.to_datetime(nuevo_valor_val)
                           # Podrías añadir más conversiones (bool, etc.)
                        except ValueError:
                            st.warning(f"No se pudieron convertir los valores al tipo {dtype_col}. Se usarán como texto.", icon="⚠️")
                            # Mantener como texto si falla la conversión específica

                        st.session_state['df'][columna_valor] = st.session_state['df'][columna_valor].replace(
                            valor_a_buscar_typed, nuevo_valor_typed
                        )
                        st.success(f"Se intentó reemplazar '{valor_a_buscar_val}' con '{nuevo_valor_val}' en la columna '{columna_valor}'.")
                        # --- Marcar para limpiar en el próximo rerun ---
                        st.session_state['replace_successful'] = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al reemplazar valor: {e}")
                        st.session_state['replace_successful'] = False
                else:
                     st.warning(f"La columna '{columna_valor}' ya no existe. Refresca la selección.")
                     st.session_state['replace_successful'] = False
            else:
                st.warning("Por favor, selecciona una columna, el valor a buscar y el nuevo valor (no deben estar vacíos).")
                st.session_state['replace_successful'] = False

    else:
        st.info("Por favor, sube un archivo primero.")