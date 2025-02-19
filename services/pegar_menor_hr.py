
import streamlit as st
import pandas as pd

def menor_hr(df):
    hrs_pessoa = df.groupby('Nome')['Duração'].sum()
    # hrs_pessoa = hrs_pessoa.apply(lambda h: int(h))
    hrs_pessoa = hrs_pessoa.iloc[-1] #OU hrs_pessoa.min()
    horas = hrs_pessoa.seconds // 3600      
    minutos = (hrs_pessoa.seconds % 3600) // 60     
    temp = horas + (minutos/100)
    mini = temp 
    # st.text(f'Menor hr: {mini}')    
    return f'{horas}h:{minutos}min'