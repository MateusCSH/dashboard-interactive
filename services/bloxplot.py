
import streamlit as st
import plotly.express as px
import pandas as pd

def bloxplot(df):
    df['Duração'] = pd.to_timedelta(df['Duração'])
    # st.write(f'Horas totais para {data}: {df["Duração"].sum()}')

    # Extrair horas e minutos
    df['horas'] = df['Duração'].dt.total_seconds() // 3600  # Horas
    df['minutos'] = (df['Duração'].dt.total_seconds() % 3600) // 60  # Minutos

    # Calcular o valor decimal (horas + minutos/100)
    df['temp'] = df['horas'] + (df['minutos'] / 100)
    
    
    
    fig = px.box(df, 
                 x='Motivo',   # Eixo X com 'Motivo'
                 y='temp',     # Eixo Y com 'Horas' totais em formato numérico
                 title="Distribuição de Duração por Motivo",
                 labels={"temp": "Duração (horas)", "Motivo": "Motivo"})  # Rótulos para os eixos

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)   