import streamlit as st
import pandas as pd

def limpiar_duplicados_ui():
    """Interfaz de usuario para la limpieza de duplicados."""
    if 'df' in st.session_state and st.session_state['df'] is not None:
        st.subheader("Limpieza de Valores Duplicados")
        columna_duplicados = st.selectbox(
            "Selecciona una columna:",
            [""] + list(st.session_state['df'].columns),
            key="selectbox_duplicados_cleaner"
        )
        if columna_duplicados:
            df = st.session_state['df'].copy()  # ¡Copia local!
            not_null_series = df[columna_duplicados].dropna()
            duplicated_mask = not_null_series.duplicated(keep=False)
            duplicate_values = not_null_series[duplicated_mask].unique()

            if len(duplicate_values) > 0:
                st.write("Valores Duplicados (sin contar nulos):")
                st.write(duplicate_values)

                opcion_conservar = st.radio(
                    f"¿Qué ocurrencia deseas conservar?",
                    ("Conservar la primera", "Conservar la última", "Eliminar todas las duplicadas"),
                    horizontal=True,
                    key="radio_duplicados_cleaner"
                )

                if st.button(
                    f"Aplicar acción en '{columna_duplicados}'",
                    key="boton_aplicar_duplicados_cleaner"
                ):
                    initial_rows = len(df)
                    if opcion_conservar == "Conservar la primera":
                        st.session_state['df'] = df.drop_duplicates(
                            subset=[columna_duplicados], keep='first'
                        ).reset_index(drop=True).copy()  # ¡Copia al actualizar!
                        eliminadas = initial_rows - len(st.session_state['df'])
                        st.success(
                            f"Se eliminaron {eliminadas} filas (primera ocurrencia conservada en '{columna_duplicados}')."
                        )
                    elif opcion_conservar == "Conservar la última":
                        st.session_state['df'] = df.drop_duplicates(
                            subset=[columna_duplicados], keep='last'
                        ).reset_index(drop=True).copy()
                        eliminadas = initial_rows - len(st.session_state['df'])
                        st.success(
                            f"Se eliminaron {eliminadas} filas (última ocurrencia conservada en '{columna_duplicados}')."
                        )
                    elif opcion_conservar == "Eliminar todas las duplicadas":
                        st.session_state['df'] = df[
                            ~df.duplicated(subset=[columna_duplicados], keep=False)
                        ].reset_index(drop=True).copy()
                        eliminadas = initial_rows - len(st.session_state['df'])
                        st.success(
                            f"Se eliminaron {eliminadas} filas (todas las duplicadas en '{columna_duplicados}')."
                        )
                    st.rerun()
            else:
                st.info(
                    f"No se encontraron duplicados (sin nulos) en '{columna_duplicados}'."
                )
    else:
        st.info("Por favor, sube un archivo primero.")


def limpiar_nulos_ui():
    """Interfaz de usuario para la limpieza de valores nulos."""
    if 'df' in st.session_state and st.session_state['df'] is not None:
        st.subheader("Limpieza de Valores Nulos")
        columna_nulos = st.selectbox(
            "Selecciona una columna:",
            [""] + list(st.session_state['df'].columns),
            key="selectbox_nulos_cleaner"
        )
        if columna_nulos:
            df = st.session_state['df'].copy()  # ¡Copia local!
            nulos_count = df[columna_nulos].isnull().sum()
            st.write(f"Número de valores nulos en '{columna_nulos}': {nulos_count}")

            opcion_nulos = st.selectbox(
                "¿Qué acción deseas realizar?",
                ("Seleccionar acción", "Eliminar filas con nulos", "Rellenar con un valor"),
                key="selectbox_accion_nulos_cleaner"
            )
            if opcion_nulos == "Eliminar filas con nulos":
                if st.button(
                    f"Eliminar nulos en '{columna_nulos}'",
                    key="boton_eliminar_nulos_cleaner"
                ):
                    initial_rows = len(df)
                    st.session_state['df'] = df.dropna(
                        subset=[columna_nulos]
                    ).reset_index(drop=True).copy()  # ¡Copia al actualizar!
                    eliminadas = initial_rows - len(st.session_state['df'])