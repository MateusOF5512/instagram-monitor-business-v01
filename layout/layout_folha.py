# Importação de Bibliotecas:
import streamlit as st
from outros.variaveis_folha import *
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from PIL import Image

from plots.plots_folha import *

## - Topo e Rodapé da Aplicação:
def topo1():
    st.markdown(html_title1, unsafe_allow_html=True)

    return None

def topo2():
    st.markdown(html_title2, unsafe_allow_html=True)

    return None

def rodape():
    st.markdown(html_rodape, unsafe_allow_html=True)
    return None

config={"displayModeBar": True,
        "displaylogo": False,
        'modeBarButtonsToRemove': ['zoom2d', 'toggleSpikelines',
                                   'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                   'hoverClosestCartesian', 'hoverCompareCartesian']}

def folha_posts(df):

    st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'"+
                ">Tabela com dados das publicações do Instagram:</h1>",
                unsafe_allow_html=True)
    simple_aggrid(df)

    st.text("")
    st.text("")


    col2A, col3A, col4A = st.columns([520, 60, 520])
    with col2A:
        st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                    ">Indicadores Chaves</h1>",
                    unsafe_allow_html=True)
        fig1, fig2 = metricas(df)
        st.plotly_chart(fig1, use_container_width=True, config=config)
        st.plotly_chart(fig2, use_container_width=True, config=config)
    with col3A:
        st.text("")
    with col4A:
        st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                    ">Análise por Tipo de Publicação</h1>",
                    unsafe_allow_html=True)
        figA4 = pie3(df)
        st.plotly_chart(figA4, use_container_width=True, config=config)  # GRÁFICO DE BARRA HORIZONTAL

    st.text("")
    st.text("")

    col2, col3, col4 = st.columns([520, 60, 520])
    with col2:
        st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                    ">Análise Temporal</h1>",
                    unsafe_allow_html=True)
        figB2 = linha(df)
        st.plotly_chart(figB2, use_container_width=True, config=config)
    with col3:
        st.text("")
    with col4:
        st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                    ">Comparação entre os Portais</h1>",
                    unsafe_allow_html=True)
        figB1 = bar_nomes(df)
        st.plotly_chart(figB1, use_container_width=True, config=config)

    st.text("")
    st.text("")

    col2, col3, col4= st.columns([520, 60, 520])
    with col2:
        st.markdown("<h1 style='font-size:140%; text-align: center; color: #5B51D8;'" +
                    ">Comparação entre os Dias da Semana</h1>",
                    unsafe_allow_html=True)
        figB1 = bar(df)
        st.plotly_chart(figB1, use_container_width=True, config=config)  # GRÁFICO DE BARRA HORIZONTAL

    with col3:
        st.text("")
    with col4:
        st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                    ">Comparação entre os Horários</h1>",
                    unsafe_allow_html=True)
        fig1 = bar_hora(df)
        st.plotly_chart(fig1, use_container_width=True, config=config)

    st.text("")
    st.text("")

    col2, col3, col4 = st.columns([520, 60, 520])
    with col2:
        st.markdown("<h1 style='font-size:140%; text-align: center; color: #5B51D8;'" +
                    ">Número de Publicações por Turno e Dia da Semana</h1>",
                    unsafe_allow_html=True)
        figC1, figC2 = map(df)

        st.plotly_chart(figC1, use_container_width=True, config=config)  # GRÁFICO DE BARRA HORIZONTAL
    with col3:
        st.text("")
    with col4:
        st.markdown("<h1 style='font-size:143%; text-align: center; color: #5B51D8;'" +
                    ">Número de Interações por Turno e Dia da Semana</h1>",
                    unsafe_allow_html=True)
        st.plotly_chart(figC2, use_container_width=True, config=config)  # GRÁFICO DE BARRA HORIZONTAL

    st.text("")
    return None


