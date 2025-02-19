
import streamlit as st
import pandas as pd

def cont(df):
    # Somar a duração total (timedelta)
    hrs_pessoa = df['Duração'].sum()

    horas = hrs_pessoa.seconds // 3600      
    minutos = (hrs_pessoa.seconds % 3600) // 60     
    temp = horas + (minutos/100)
    # st.text(f'Tempo em horas e minutos, método anterior: {temp}')
    text_transform = f'{horas}h:{minutos}m'
    # st.text(f'Horas transformadas: {text_transform}')

    return text_transform