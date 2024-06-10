import streamlit as st
import pandas as pd
import plost

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load data
seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])
rend_usuarios = pd.read_csv('Rend_usuarios.csv')

# Extract unique values for dropdown menus
users = rend_usuarios['Usuario'].unique()
years = rend_usuarios['Mes_Año'].str[:4].unique()
months = rend_usuarios['Mes_Año'].str[5:7].unique()

st.sidebar.header('Dashboard `version 2`')

st.sidebar.subheader('Select User, Year, and Month')
selected_user = st.sidebar.selectbox('User', users)
selected_year = st.sidebar.selectbox('Year', years)
selected_month = st.sidebar.selectbox('Month', months)

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

# Filter data based on selections
filtered_data = rend_usuarios[(rend_usuarios['Usuario'] == selected_user) & 
                              (rend_usuarios['Mes_Año'].str[:4] == selected_year) & 
                              (rend_usuarios['Mes_Año'].str[5:7] == selected_month)]

if not filtered_data.empty:
    metros_cuadrados = filtered_data['Metros cuadrados reales por rollo'].values[0]
    tiempo_horas = filtered_data['tiempo_en_horas'].values[0]
    metros_por_hora = filtered_data['metros_por_hora'].values[0]
else:
    metros_cuadrados = tiempo_horas = metros_por_hora = 0

# Row A
st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Metros Cuadrados", f"{metros_cuadrados:,.2f} m²")
col2.metric("Tiempo en Horas", f"{tiempo_horas:,.2f} horas")
col3.metric("Metros por Hora", f"{metros_por_hora:,.2f} m/h")

# Row B
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
    # Assuming the 'Litros (1).csv' file is already loaded as 'data'
    data = pd.read_csv('Litros (1).csv')
    litros_por_linea = data.groupby('Línea')['Ctd.total reg.'].sum()
    total_litros = litros_por_linea.sum()
    porcentajes_por_linea = (litros_por_linea / total_litros) * 100
    porcentajes_por_linea = porcentajes_por_linea.reset_index()
    porcentajes_por_linea.columns = ['Línea', 'Porcentaje']
    
    plost.donut_chart(
        data=porcentajes_por_linea,
        theta='Porcentaje',
        color='Línea',
        legend='bottom', 
        use_container_width=True)

# Row C
st.markdown('### Line chart')
st.line_chart(seattle_weather, x = 'date', y = plot_data, height = plot_height)
