# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Z6biFtMh7JAJOotqtg-FqjrxJFcMGKbO
"""

import streamlit as st
import pandas as pd
import numpy as np

def cargar_csv():
    uploaded_file = st.file_uploader("Sube tu archivo CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            return df
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")
            return None
    else:
        return None

def filtrar_por_estado(df):
    estado = st.selectbox("Selecciona el estado del pedido", df['Estado'].unique())
    filtrados = df[df['Estado'] == estado]
    st.write(f"Pedidos con estado '{estado}':")
    st.dataframe(filtrados)
    return filtrados

def calcular_tiempos_entrega(df):
    df['Fecha_Pedido'] = pd.to_datetime(df['Fecha_Pedido'])
    df['Fecha_entrega'] = pd.to_datetime(df['Fecha_entrega'], errors='coerce')

    # Calcular tiempos de entrega
    df['Tiempo_Entrega'] = (df['Fecha_entrega'] - df['Fecha_Pedido']).dt.days
    tiempos_validos = df['Tiempo_Entrega'].dropna()

    if not tiempos_validos.empty:
        tiempo_promedio = tiempos_validos.mean()
        st.success(f"El tiempo promedio de entrega es de {tiempo_promedio:.2f} días.")
    else:
        st.warning("No hay datos válidos para calcular el tiempo promedio de entrega.")

def generar_informe_descargable(df):
    if st.button("Generar informe descargable"):
        informe_csv = df.to_csv(index=False)
        st.download_button(
            label="Descargar informe CSV",
            data=informe_csv,
            file_name="informe_pedidos.csv",
            mime="text/csv"
        )

def main():
    st.title("Gestión de Pedidos")
    st.write("Carga un archivo CSV con la estructura especificada para comenzar.")

    # Cargar datos
    df = cargar_csv()

    if df is not None:
        st.subheader("Datos cargados")
        st.dataframe(df)

        # Filtrar por estado
        st.subheader("Filtrar pedidos por estado")
        pedidos_filtrados = filtrar_por_estado(df)

        # Calcular tiempos promedio de entrega
        st.subheader("Tiempos promedio de entrega")
        calcular_tiempos_entrega(df)

        # Generar informe descargable
        st.subheader("Informe descargable")
        generar_informe_descargable(pedidos_filtrados)

if __name__ == "__main__":
    main()