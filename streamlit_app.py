import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# Generar datos aleatorios para probar la gráfica
dates = pd.date_range(start='2021-01-01', periods=12, freq='M')
values = np.random.randint(1000, 10000, size=(12,))
test_data = pd.DataFrame({'date': dates, 'Ctd.total reg.': values})

# Mostrar datos aleatorios generados
st.write("Datos generados aleatoriamente:")
st.write(test_data)

# Verificar tipos de datos
st.write("Tipos de datos en test_data:")
st.write(test_data.dtypes)

# Graficar usando st.line_chart
st.markdown('### Gráfica de datos aleatorios')
st.line_chart(test_data.set_index('date')['Ctd.total reg.'])
