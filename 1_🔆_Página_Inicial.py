# BIBLIOTECAS USADAS

import streamlit as st
from PIL import Image

im = Image.open("image/instagram.png")
st.set_page_config(page_title="Instagram Monitor Interativo", page_icon=im, layout="wide")

st.markdown(""" <style>
        footer {visibility: hidden;}
        </style> """, unsafe_allow_html=True)

from layout.layout_folha import *
from plots.plots_folha import *
from outros.variaveis_folha import *


df = get_data(path_todos)

df = df[['Nome', 'time', 'descricao', 'likes', 'comentarios', 'inter', 'tipo',
         'dia', 'hora', 'semana', 'Turno', 'shortcode', 'ID post', 'UNIDADE']]

with st.sidebar:
    st.markdown(html_title_sidebar, unsafe_allow_html=True)
    st.markdown("")
    st.markdown(html_sub1_sidebar, unsafe_allow_html=True)

    graficos = ["Gráfico de Barra", "Gráfico de Linha", "Mapa de Calor", "Nuvem de Palavras"]

    grafico = st.selectbox("Selecione o tipo de Gráfico:", graficos)

    if grafico == "Gráfico de Barra":
        df_x = df[['Nome', 'tipo', 'shortcode', 'dia', 'hora','semana','Turno']]
        optionx = st.selectbox('Selecione coluna para o Eixo X:', df_x.columns.unique(), index=0)

        df_y = df[['likes', 'comentarios', 'inter']]
        optiony = st.selectbox('Selecione coluna para o Eixo Y:', df_y.columns.unique(), index=0)
        st.markdown("")

        formato = st.radio("Selecione o formato para o Eixo Y:",
                 options=["Total de Atividades", "Média de Atividades", "Atividades por Publicação"])

    elif grafico == "Gráfico de Linha":
        df_x_linha = df[['descricao', 'shortcode', 'time', 'dia']]
        optionx_linha = st.selectbox('Selecione coluna para o Eixo X: - diferente',
                                     df_x_linha.columns.unique(), index=2)

        df_y_linha = df[['likes', 'comentarios', 'inter']]
        optiony_linha = st.selectbox('Selecione coluna para o Eixo Y:',
                               df_y_linha.columns.unique(), index=0)
        st.markdown("")

        formato_linha = st.radio("Selecione o formato para o Eixo Y:",
                           options=["Total de Atividades", "Média de Atividades", "Atividades por Publicação"])

    elif grafico == "Mapa de Calor":
        df_heatmap = df[['likes', 'comentarios', 'inter']]
        option_heatmap = st.selectbox('Selecione a variável para o Mapa de Calor:',
                                     df_heatmap.columns.unique(), index=0)

    st.markdown("")
    st.markdown("")
    st.markdown("")

    icon = Image.open("image/InstaMonitor.png")
    st.image(icon, use_column_width=True, caption="Versão: 0.0.2 ")
    st.markdown("""---""")


# APLICAÇÃO
topo()
st.markdown("""---""")

all_Nomes = df.Nome.unique().tolist()
selected_Nomes = st.multiselect("Selecione o Portal da sua análise", options=all_Nomes, default=all_Nomes)
df_select = df[df.Nome.isin(selected_Nomes)]

selected_rows = folha_tabela(df_select)


if len(selected_rows) != 0:
    if grafico == "Gráfico de Barra":
        fig1 = plot_bar(formato, selected_rows, optionx, optiony)
        st.plotly_chart(fig1, use_container_width=True)

    elif grafico == "Gráfico de Linha":
        fig2 = plot_line(selected_rows, optionx_linha, optiony_linha)
        st.plotly_chart(fig2, use_container_width=True)

    elif grafico == "Mapa de Calor":
        fig3 = plot_hotmap(df_select, option_heatmap)
        st.plotly_chart(fig3, use_container_width=True)

    elif grafico == "Nuvem de Palavras":
        fig4 = plot_wordcoud(selected_rows)
        st.pyplot(fig4)


if len(selected_rows) == 0:

    if grafico == "Gráfico de Barra":
        fig3A2 = plot_bar(formato, df_select, optionx, optiony)
        st.plotly_chart(fig3A2, use_container_width=True)

    elif grafico == "Gráfico de Linha":
        fig2 = plot_line(df_select, optionx_linha, optiony_linha)
        st.plotly_chart(fig2, use_container_width=True)

    elif grafico == "Mapa de Calor":
        fig3 = plot_hotmap(df_select, option_heatmap)
        st.plotly_chart(fig3, use_container_width=True)

    elif grafico == "Nuvem de Palavras":
        fig4 = plot_wordcoud(df_select)
        st.pyplot(fig4)

st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
rodape()