# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Z6biFtMh7JAJOotqtg-FqjrxJFcMGKbO
"""

import streamlit as st
import pandas as pd
from io import BytesIO

def generar_informe_csv(df):
    """Genera un archivo CSV descargable."""
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output

def calcular_tiempos_entrega(df):
    """Calcula el tiempo promedio de entrega en días."""
    df["Fecha_Pedido"] = pd.to_datetime(df["Fecha_Pedido"], errors="coerce")
    df["Fecha_entrega"] = pd.to_datetime(df["Fecha_entrega"], errors="coerce")
    df["Tiempo_Entrega"] = (df["Fecha_entrega"] - df["Fecha_Pedido"]).dt.days
    return df["Tiempo_Entrega"].mean()

# Configuración de la app
st.title("Gestión de Pedidos")
st.sidebar.header("Cargar Archivo CSV")

# Subir archivo CSV
archivo_csv = st.sidebar.file_uploader("Selecciona un archivo CSV", type="csv")

if archivo_csv is not None:
    # Cargar datos
    df = pd.read_csv(archivo_csv)

    st.write("### Datos Cargados:")
    st.dataframe(df.head())

    # Filtrar por estado
    estados = df["Estado"].unique()
    estado_seleccionado = st.sidebar.selectbox("Filtrar por Estado", options=estados)

    df_filtrado = df[df["Estado"] == estado_seleccionado]

    st.write(f"### Pedidos con Estado: {estado_seleccionado}")
    st.dataframe(df_filtrado)

    # Calcular tiempos promedio de entrega
    if "Fecha_entrega" in df.columns and "Fecha_Pedido" in df.columns:
        tiempo_promedio = calcular_tiempos_entrega(df)
        if pd.notnull(tiempo_promedio):
            st.write(f"### Tiempo Promedio de Entrega: {tiempo_promedio:.2f} días")
        else:
            st.write("### No hay datos suficientes para calcular el tiempo promedio de entrega.")
    else:
        st.write("### Las columnas de fechas no están disponibles en el archivo cargado.")

    # Generar informe descargable
    informe = generar_informe_csv(df_filtrado)
    st.download_button(
        label="Descargar Informe CSV",
        data=informe,
        file_name="informe_pedidos.csv",
        mime="text/csv"
    )
else:
    st.write("### Por favor, carga un archivo CSV para comenzar.")