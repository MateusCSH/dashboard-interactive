
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from services.conversao_hrs import conversor
from services.gráfico_bar_vert import grafico_barras
from services.gráfico_pizza import grafico_pizza
from services.calcular_hrs import cont
from services.pegar_menor_hr import menor_hr, menor_private
from services.pegar_maior_hr import maior_hr, maior_private
from services.three_cards import cards
from services.card_qtd_monitor import card_qtd_monitor
from services.bloxplot import bloxplot
from services.gráfico_dias_semana import dias_semana

# LEMBRE DE POR NA PASTA PRICIPAL E DEPOIS RODAR O COMANDO:
# streamlit run app/main.py
# Na pasta pricipal acesse o diretorio e o arquivo já inicializando o app.

# Separar por pessoa
# Realizar soma das horas [saida - entrada], limitando a 6 horas diárias

with open("style.css", 'r',encoding='utf') as r:
    st.markdown(f"<style>{r.read()}</style>",unsafe_allow_html=True)

st.markdown('''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    ''',unsafe_allow_html=True)


file = st.sidebar.file_uploader('Baixar arquivo', type=['csv'])

if file is not None:
    df = pd.read_csv(file, sep=',')
    # df.columns = ['Nome', 'Data', 'Horário de Saída', 'Motivo', 'Horário de entrada']
    print("-"*50)
    print("df: ", df)
    print(df.columns)
    df = df[["Nome", "Data", "Motivo", "Horário de entrada", "Horário de Saída"]]
    print('Dataframe que vamos trabalhar: ', df)   

    
    # Converter as colunas para datetime e time
    conversor(df)

    df = df[["Nome", "Data", "Motivo", "Horário de entrada", "Horário de Saída", "Duração (hh:mm)"]]
    print(df)
    
    # st.dataframe(df)


    ### RESTANTE

    # Converter "Duração (hh:mm)" para timedelta
    df['Duração'] = df['Duração (hh:mm)'].apply(lambda x: timedelta(hours=int(x.split(':')[0]), minutes=int(x.split(':')[1])))

    st.sidebar.markdown('Selecione o que deseja')
    opcao = st.sidebar.radio('Selecione a opção que deseja ver', ['Gráfico','Cards'])
    if opcao == 'Gráfico':
        opcao_gp = st.radio('Selecione o tipo:', ['Relatório gráfico', 'Relatório escrito'], horizontal=True)
        
        if opcao_gp == 'Relatório gráfico':

            # GRÁFICO COM AS HORAS POR PESSOA.
            df_filt = df.groupby('Nome',)['Duração'].sum().reset_index()

            # Agora, converta a coluna 'Duração' (Timedelta) para horas numéricas
            df_filt['Horas'] = df_filt['Duração'].apply(lambda td: td.total_seconds() / 3600)

            # Agora converta a coluna 'Horas' para horas no formato 'hh:mm' para exibição no gráfico
            df_filt['Horas (hh:mm)'] = df_filt['Horas'].apply(lambda h: f"{int(h):02}:{int((h % 1) * 60):02}")
            # st.text(f"Duração total para {df_filt['Horas (hh:mm)']}")    

            # Criar gráfico de barras com Plotly
            print(df_filt)

            st.markdown(f"""<div class = 'marcacao'>
                        <p>RELATÓRIO GRÁFICO TEMPO DE PERMANÊNCIA</p>
                        </div>""", unsafe_allow_html=True)
            grafico_barras(df_filt)


            # GRÁFICO DE PIZZA
            st.markdown(f"""<div class = 'marcacao'>
                        <p>RELATÓRIO GRÁFICO TEMPO DE PERMANÊNCIA</p>
                        </div>""", unsafe_allow_html=True)
            grafico_pizza(df_filt)


            # Atendimentos por Dia.
            st.markdown(f"""<div class = 'marcacao'>
                        <p>Atendimentos por Dia</p>
                        </div>""", unsafe_allow_html=True)
            atendimentos_por_dia = df.groupby('Data').size()
            st.line_chart(atendimentos_por_dia)

            # motivos mais frequentes.
            st.markdown(f"""<div class = 'marcacao'>
                        <p>motivos mais frequentes</p>
                        </div>""", unsafe_allow_html=True)
            motivos_contagem = df['Motivo'].value_counts().reset_index()
            st.bar_chart(motivos_contagem.set_index('Motivo'), color='rgb(135, 206, 235)')


            # dias mais frequentes.
            st.markdown(f"""<div class = 'marcacao'>
                        <p>Dias mais frequentes</p>
                        </div>""", unsafe_allow_html=True)
            dias_semana(df)
            


            # BLOXBPLOT.
            st.markdown(f"""<div class = 'marcacao'>
                        <p>Gráfico BloxPlot</p>
                        </div>""", unsafe_allow_html=True)
            bloxplot(df)


            df["Duração_min"] = df["Duração"].dt.total_seconds() / 60  # Converter para minutos
            anomalias = df[(df["Duração_min"] > (60*5)) | (df["Duração_min"] < 15)]
            if not anomalias.empty:
                st.warning("⚠️ Registros com durações atípicas:")
                st.dataframe(anomalias)

                  


        if opcao_gp == 'Relatório escrito':


                # Pega o tempo total da base de dados e realiza o tratamento.
                # hrs_transformadas = cont(df)

                

                # Criar cards para mostrar a quantidade de hrs por motivo
                motivo = st.selectbox('Selecione o motivo', options=sorted(df['Motivo'].unique()))
                df_filtrado2 = df[df['Motivo'] == motivo]
                hrs_motivo_x = cont(df_filtrado2)
                # st.write(f'Horas totais para {motivo}: {hrs_motivo_x}')          
                
                # Função para mostrar menor tempo
                smalltime = menor_private(df_filtrado2)

                # Função para mostrar maior tempo
                biggesttime = maior_private(df_filtrado2)
                
                st.markdown(f""" <div class='container_cards_externo'>
                            <div class='container_cards_interno'> Horas totais 
                            <p>{(hrs_motivo_x)}</p> </div>
                            <div class='container_cards_interno'> Maior tempo 
                            <p>{biggesttime}</p> </div>
                            <div class='container_cards_interno'> Menor tempo 
                            <p>{smalltime}</p> </div></div>""", unsafe_allow_html=True)




                # CRIAR CAMPO DE BUSCA POR NOME, MOSTRAR DATASET FILTRADO, HOARS DA PESSOA.. INFORMAÇÕES.
                available_dates = df['Data'].dt.date.unique() 
                # data = st.date_input('Selecione a data de pesquisa', min_value=df['Data'].min().date(), max_value=df['Data'].max().date())
                data = st.date_input(
                    'Selecione a data de pesquisa',
                    min_value=available_dates.min(),
                    max_value=available_dates.max(),
                    value=available_dates.min()  # Valor inicial padrão
)
                if data in available_dates:
                    df_filt_date = df[df['Data'].dt.date == data]
                    st.dataframe(df_filt_date)
                    df_filt_date['Duração'] = pd.to_timedelta(df_filt_date['Duração'])
                    # st.write(f'Horas totais para {data}: {df_filt_date["Duração"].sum()}')

                    # Extrair horas e minutos
                    df_filt_date['horas'] = df_filt_date['Duração'].dt.total_seconds() // 3600  # Horas
                    df_filt_date['minutos'] = (df_filt_date['Duração'].dt.total_seconds() % 3600) // 60  # Minutos

                    # Calcular o valor decimal (horas + minutos/100)
                    df_filt_date['temp'] = df_filt_date['horas'] + (df_filt_date['minutos'] / 100)

                    # Encontrar o maior valor de tempo
                    max_temp = df_filt_date['temp'].max()
                    min_temp = df_filt_date['temp'].min()

                    # Extrair horas e minutos do maior e menor valor
                    horas = int(max_temp)
                    minutos = int((max_temp - horas) * 100)
                    min_horas = int(min_temp)
                    min_minutos = int((min_temp - min_horas) * 100)

                    # Exibir o maior tempo no formato hh:mm
                    # st.text(f'Maior hr: {horas}h:{minutos:02d}min')
                    # st.text(f'Menor hr: {min_horas}h:{min_minutos:02d}min')




                    tempo_total = df_filt_date['Duração'].sum()
                    
                    # Extrair horas e minutos do total
                    horas_totais = tempo_total.total_seconds() // 3600
                    minutos_totais = (tempo_total.total_seconds() % 3600) // 60
                    # st.text(f'Tempo total: {int(horas_totais)}h:{int(minutos_totais):02d}min')


                    # POR DADOS NO CARD            
                    
                    h_tot = f'{horas_totais:.0f}h:{minutos_totais:.0f}min'
                    h_m = f'{horas}h:{minutos:.0f}min'
                    min_h_min_m = f'{min_horas}h:{min_minutos:.0f}min'
                    cards(df_filt_date, h_tot, h_m, min_h_min_m)

                

                

                    st.markdown(f"""<div class = 'marcacao'>
                            <p>TEMPO TOTAL</p>
                            </div>""", unsafe_allow_html=True)
                    
                    hrs_motivo_x = cont(df)                 
                    # Função para mostrar menor tempo
                    smalltime = menor_hr(df)
                    # Função para mostrar maior tempo
                    biggesttime = maior_hr(df)

                    cards(df, hrs_motivo_x, biggesttime, smalltime)
                
                else:
                    st.warning("Data selecionada não encontrada na base de dados!")



                # selected_color = st.radio('Selecione:', ['Green', 'Red', 'Black'], key='styledradio', horizontal=True)

                select_name = st.text_input('Digite o nome para busca:', key='namekey', max_chars=50)
                name = select_name.strip().lower()
                # Verifique se o nome não está vazio
                if select_name: 
                    # Verifique se o nome existe na coluna "Nome"
                    df_filtered = df[df['Nome'].str.lower().str.contains(name, na=False)]
                    if not df_filtered.empty:
                        st.write(df_filtered)
                        qtd_hrs_nome = cont(df_filtered)
                        maior_p_nome = maior_private(df_filtered)
                        menor_p_nome = menor_private(df_filtered)

                        cards(df_filtered, qtd_hrs_nome, maior_p_nome, menor_p_nome)
                        
                    else:
                        st.error(f" 🚷:blue[{select_name}] não foi encontrado. Digite um nome valido ❗")
                else:
                    st.warning("Digite um nome para buscar.")  

                st.markdown('<i class="fa-solid fa-down-long"></i> Texto com ícone', unsafe_allow_html=True)




                

    if opcao == 'Cards':
        
        st.title('Cards')

        # MOSTRAR QUANTIDADE DE MONITORES,
        qtd_monitor = df['Nome'].count()
        # st.header(qtd_monitor)

        qtd_vezes = df.groupby('Nome')['Nome'].count()
        nome_max = qtd_vezes.idxmax()
        nome_min = qtd_vezes.idxmin()
        # st.write(qtd_vezes.max())
        # st.write(nome)

        card_qtd_monitor(df, qtd_monitor, qtd_vezes.max(), nome_max)
        card_qtd_monitor(df, qtd_monitor, qtd_vezes.min(), nome_min)

        VIDEO_URL = "https://www.youtube.com/watch?v=bbOw3Q2cRrw"
        st.video(VIDEO_URL)



        
                





                

                # def icon_button(icon, text, key):
                #     st.markdown(f"""
                #     <style>
                #     #{key} {{
                #         border: 2px solid #4b0082;
                #         border-radius: 5px;
                #         padding: 10px 20px;
                #         cursor: pointer;
                #         transition: all 0.3s;
                #     }}
                #     #{key}:hover {{ background: #4b0082; color: white; }}
                #     </style>
                #     <div id="{key}" onclick="document.getElementById('{key}-hidden').click()">
                #         <i class="{icon}"></i> {text}
                #     </div>
                #     """, unsafe_allow_html=True)
                    
                #     return st.checkbox("", key=f"{key}-hidden", label_visibility="hidden")

                # if icon_button("fas fa-download", "Download", "btn1"):
                #     st.write("Download iniciado!")
                   










