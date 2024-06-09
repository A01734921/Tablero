import streamlit as st
import pandas as pd
import plost
import matplotlib.pyplot as plt
import os

# Título de la aplicación
st.title('Tendencia de Consumos Mensuales de las 10 Pinturas más Utilizadas')

# Verificar si el archivo CSV existe
file_path = 'Litros (1).csv'
if not os.path.exists(file_path):
    st.error(f"Archivo {file_path} no encontrado. Asegúrate de que el archivo CSV esté en el mismo directorio que el script.")
else:
    # Cargar los datos
    data = pd.read_csv(file_path)

    # Convertir la columna de fecha a tipo datetime y extraer año y mes
    data['Registrado'] = pd.to_datetime(data['Registrado'], format='%Y-%m')
    data['Año-Mes'] = data['Registrado'].dt.to_period('M')

    # Calcular el consumo total por material
    consumo_total_por_material = data.groupby('Texto breve de material')['Ctd.total reg.'].sum()

    # Obtener las 10 pinturas con mayor consumo
    top_10_pinturas = consumo_total_por_material.nlargest(10).index

    # Filtrar los datos para las 10 pinturas más utilizadas
    data_top_10 = data[data['Texto breve de material'].isin(top_10_pinturas)]

    # Agrupar por mes y material para calcular el consumo mensual
    consumo_mensual = data_top_10.groupby(['Año-Mes', 'Texto breve de material'])['Ctd.total reg.'].sum().unstack().fillna(0)

    # Crear el gráfico
    st.write('Este gráfico muestra la tendencia de consumo mensual de las 10 pinturas más utilizadas.')

    plt.figure(figsize=(10, 6))
    for material in consumo_mensual.columns:
        plt.plot(consumo_mensual.index.to_timestamp(), consumo_mensual[material], label=material)

    plt.xlabel('Mes')
    plt.ylabel('Consumo Total')
    plt.title('Tendencia de Consumo Mensual')
    plt.legend(loc='upper right')
    plt.grid(True)
    st.pyplot(plt)

