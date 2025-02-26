
import streamlit as st
import pandas as pd
import plotly.express as px


def grafico_pizza(df):
    fig = px.pie(df, values='Horas', names='Nome',
             title='Porcentagem tempo de monitoria',
             hover_data=['Horas'], labels={'Nome'})
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig)