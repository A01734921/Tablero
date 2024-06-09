import streamlit as st
import pandas as pd
import plost

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.sidebar.header('Dashboard `version 2`')

st.sidebar.subheader('Heat map parameter')
time_hist_color = st.sidebar.selectbox('Color by', ('temp_min', 'temp_max')) 

st.sidebar.subheader('Donut chart parameter')
donut_theta = st.sidebar.selectbox('Select data', ('q2', 'q3'))

st.sidebar.subheader('Line chart parameters')
plot_data = st.sidebar.multiselect('Select data', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'])
plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)

st.sidebar.markdown('''
---
Created with ❤️ by [Data Professor](https://youtube.com/dataprofessor/).
''')


# Row A
st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

# Row B
seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])
stocks = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/stocks_toy.csv')

c1, c2 = st.columns((7,3))
with c1:
    st.markdown('### Heatmap')
    plost.time_hist(
    data=seattle_weather,
    date='date',
    x_unit='week',
    y_unit='day',
    color=time_hist_color,
    aggregate='median',
    legend=None,
    height=345,
    use_container_width=True)
with c2:
    st.markdown('### Donut chart')
    plost.donut_chart(
        data=stocks,
        theta=donut_theta,
        color='company',
        legend='bottom', 
        use_container_width=True)

# Row C
st.markdown('### Line chart')
st.line_chart(seattle_weather, x = 'date', y = plot_data, height = plot_height)

# Título de la aplicación
st.title('Tendencia de Consumos Mensuales de las 10 Pinturas más Utilizadas')

# Cargar los datos
file_path = 'Litros (1).csv'  # Asegúrate de que el archivo CSV esté en el mismo directorio que el script
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

