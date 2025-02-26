

import pandas as pd
import streamlit as st


def card_qtd_monitor(df, qtd, vezes, nome):
    a = 1+2
    st.markdown(f""" <div class='monitor_externo'>
                    <div class='monitor_interno'> Quantidade de monitores 
                    <p>{(qtd)}</p> </div>
                    <div class='monitor_interno'> Pessoa que mais visitou 
                    <p>{nome}</p> </div>
                    <div class='monitor_interno'> Quantidade 
                    <p>{vezes}</p> </div></div>""", unsafe_allow_html=True)
