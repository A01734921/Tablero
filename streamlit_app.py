import streamlit as st
import pandas as pd
import numpy as np
import plost
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Estilo personalizado para matplotlib
def apply_custom_style():
    plt.rcParams.update({
        "axes.facecolor": "#f5a623",
        "axes.edgecolor": "white",
        "axes.labelcolor": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "figure.facecolor": "#f5a623",
        "grid.color": "gray",
        "grid.linestyle": "--",
        "grid.linewidth": 0.5,
        "lines.linewidth": 2,
        "lines.color": "#f5a623",  # Ternium orange
        "legend.facecolor": "#f5a623",
        "legend.edgecolor": "white",
        "text.color": "white"
    })

apply_custom_style()

# Color naranja de Ternium
ternium_orange = '#e31837'

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load data
seattle_weather = pd.read_csv('seattle-weather.csv', parse_dates=['date'])
rend_usuarios = pd.read_csv('Rend_usuarios.csv')
paint_data = pd.read_csv('LitrosFiltrada (1).csv', parse_dates=['Registrado'])

# Convert 'Registrado' column to datetime if not already
paint_data['Registrado'] = pd.to_datetime(paint_data['Registrado'], errors='coerce')

# Extract unique values for dropdown menus
users = rend_usuarios['Usuario'].unique()
years = rend_usuarios['Mes_Año'].str[:4].unique()
months = rend_usuarios['Mes_Año'].str[5:7].unique()
lines = paint_data['Línea'].unique()
paints = paint_data['Texto breve de material'].unique()
paint_years = paint_data['Registrado'].dt.year.dropna().unique()

st.sidebar.header('Dashboard `version 2`')

st.sidebar.subheader('Select User, Year, and Month')
selected_user = st.sidebar.selectbox('User', users)
selected_year = st.sidebar.selectbox('Year', years)
selected_month = st.sidebar.selectbox('Month', months)

st.sidebar.subheader('Heat map parameter')
time_hist_color = st.sidebar.selectbox('Color by', ('temp_min', 'temp_max'))

st.sidebar.subheader('Donut chart parameter')
donut_theta = st.sidebar.selectbox('Select data', ('q2', 'q3'))

st.sidebar.subheader('Paint Consumption Trend')
paint_option = st.sidebar.selectbox('Select Paint or All', ['All'] + list(paints))
line_option = st.sidebar.selectbox('Select Line or All', ['All'] + list(lines))
year_option = st.sidebar.selectbox('Select Year or All', ['All'] + list(paint_years))

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
    st.markdown('### Investment by Paint')
    if paint_option != 'All':
        investment_data = paint_data[paint_data['Texto breve de material'] == paint_option]
    elif line_option != 'All':
        investment_data = paint_data[paint_data['Línea'] == line_option]
    elif year_option != 'All':
        investment_data = paint_data[paint_data['Registrado'].dt.year == int(year_option)]
    else:
        investment_data = paint_data

    # Verify the existence of 'Valor total' column
    if '    Valor var.' in investment_data.columns:
        investment_summary = investment_data.groupby('Texto breve de material')['    Valor var.'].sum().reset_index()
        fig, ax = plt.subplots()
        investment_summary.plot(kind='bar', x='Texto breve de material', y='    Valor var.', ax=ax, color=ternium_orange, legend=False)
        ax.set_title('Inversión en las Top 20 Pinturas', fontsize=16, fontweight='bold', color='white')
        ax.set_xlabel('Pintura', fontsize=14, fontweight='bold', color='white')
        ax.set_ylabel('Valor', fontsize=14, fontweight='bold', color='white')
        ax.tick_params(axis='x', colors='white', rotation=45)
        ax.tick_params(axis='y', colors='white')
        ax.get_yaxis().get_major_formatter().set_scientific(False)
        for tick in ax.get_xticklabels():
            tick.set_horizontalalignment('right')
        st.pyplot(fig)
    else:
        st.write("The 'Valor total' column is not found in the dataset.")

with c2:
    st.markdown('### Donut chart')
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

# Row C: Paint consumption trend line chart
st.markdown('### Paint Consumption Line Chart')

# Filter data based on selections
if paint_option == 'All' and line_option == 'All' and year_option == 'All':
    trend_data = paint_data
elif paint_option == 'All' and line_option == 'All':
    trend_data = paint_data[paint_data['Registrado'].dt.year == int(year_option)]
elif paint_option == 'All' and year_option == 'All':
    trend_data = paint_data[paint_data['Línea'] == line_option]
elif line_option == 'All' and year_option == 'All':
    trend_data = paint_data[paint_data['Texto breve de material'] == paint_option]
elif paint_option == 'All':
    trend_data = paint_data[(paint_data['Línea'] == line_option) & (paint_data['Registrado'].dt.year == int(year_option))]
elif line_option == 'All':
    trend_data = paint_data[(paint_data['Texto breve de material'] == paint_option) & (paint_data['Registrado'].dt.year == int(year_option))]
elif year_option == 'All':
    trend_data = paint_data[(paint_data['Texto breve de material'] == paint_option) & (paint_data['Línea'] == line_option)]
else:
    trend_data = paint_data[(paint_data['Texto breve de material'] == paint_option) & 
                            (paint_data['Línea'] == line_option) & 
                            (paint_data['Registrado'].dt.year == int(year_option))]

# Summarize data by month
trend_data = trend_data.copy()  # Avoid SettingWithCopyWarning
trend_data['Month'] = trend_data['Registrado'].dt.to_period('M')
monthly_trend = trend_data.groupby('Month')['Ctd.total reg.'].sum().reset_index()
monthly_trend['Month'] = monthly_trend['Month'].dt.to_timestamp()

# Asegurar que 'Month' es el índice
monthly_trend.set_index('Month', inplace=True)

# Graficar si hay datos disponibles
if not monthly_trend.empty:
    fig, ax = plt.subplots()
    monthly_trend.plot(ax=ax, color=ternium_orange, legend=False)
    ax.set_title('Tendencia de Consumo de Pintura', fontsize=16, fontweight='bold', color='white')
    ax.set_xlabel('Mes', fontsize=14, fontweight='bold', color='white')
    ax.set_ylabel('Cantidad Total Registrada', fontsize=14, fontweight='bold', color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    # Agregar leyenda personalizada
    ax.legend(['Ctd. total reg.'], loc='upper right', facecolor='#0e1117', edgecolor='white', fontsize=12)
    st.pyplot(fig)
else:
    st.write("No data available for the selected options.")
