
import pandas as pd
import streamlit as st


def cards(df, All, biggesttime, smalltime):
    st.markdown(f""" <div class='container_cards_externo'>
                    <div class='container_cards_interno'> Horas totais 
                    <p>{(All)}</p> </div>
                    <div class='container_cards_interno'> Maior tempo 
                    <p>{biggesttime}</p> </div>
                    <div class='container_cards_interno'> Menor tempo 
                    <p>{smalltime}</p> </div></div>""", unsafe_allow_html=True)