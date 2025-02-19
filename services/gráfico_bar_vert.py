
import streamlit as st
import pandas as pd
import plotly.express as px


def grafico_barras(df_filt):
    fig = px.bar(
        df_filt,
        x='Nome',
        y='Horas',  # A coluna 'Duração' será usada para o valor numérico (em horas)
        text='Horas (hh:mm)',  # Aqui estamos usando a coluna com a conversão para exibir no gráfico
        color='Nome',  # Adiciona cores diferentes para cada pessoa
        title='Duração Total por Pessoa (em Horas)',
        labels={'Nome': 'Pessoa', 'Horas': 'Horas Totais'}        
    )

    # Personalizar layout
    fig.update_traces(texttemplate='%{text}', textposition='outside')  # Mostrar valores no topo das barras
    fig.update_layout(
        xaxis_title='Monitores',
        yaxis_title='Horas Totais',
        showlegend=False,  # Esconde a legenda (opcional)
        title_x=0.5,  # Centralizar título
        yaxis=dict(tickformat=".1f")
        
    )

    # Mostrar gráfico no Streamlit
    st.plotly_chart(fig)