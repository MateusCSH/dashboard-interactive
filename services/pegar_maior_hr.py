
import streamlit as st
import pandas as pd
from datetime import timedelta

def maior_hr(df):
    # return df['max_temp'].max()

    hrs_pessoa = df.groupby('Nome')['Duração'].sum()
    hrs_pessoa = hrs_pessoa.iloc[0]  #OU hrs_pessoa.max()
    horas = hrs_pessoa.seconds // 3600      
    minutos = (hrs_pessoa.seconds % 3600) // 60     
    temp = horas + (minutos/100)
    mini = temp 
    # st.text(f'Maior hr: {horas}h:{minutos}min')    
    return f'{horas}h:{minutos}min'



# Não vai precisar de usar pois os valores são somados por dia, ou seja
# dia 1 -> uma pessoa foi 2x e ficou: 1h e 3hrs, somando 4 hrs. Não tem porquê pegar apenas 1h já que no dia
# ela ficou 4hrs.
def maior_private(df):

    df['Duração'] = pd.to_timedelta(df['Duração (hh:mm)'].str.replace(':', 'h') + 'm')

    # Encontrar a maior duração
    maior_duracao = df['Duração'].min()

    # Formatar a saída
    horas = maior_duracao.components.hours
    minutos = maior_duracao.components.minutes
    print(f"Maior duração: {horas:02}:{minutos:02}")
    
    

    st.text(f"Maior duração: {horas:02}:{minutos:02}")
    