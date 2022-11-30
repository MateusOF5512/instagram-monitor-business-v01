# BIBLIOTECAS USADAS

import streamlit as st
from PIL import Image
import datetime

im = Image.open("image/instagram.png")
st.set_page_config(page_title="Instagram Monitor Interativo", page_icon=im, layout="wide")

st.markdown(""" <style>
        footer {visibility: hidden;}
        </style> """, unsafe_allow_html=True)

from layout.layout_folha import *
from plots.plots_folha import *
from outros.variaveis_folha import *


df = get_data(path_todos)
df = df.reset_index()

df['link'] = 'www.instagram.com/p/' + df['shortcode'].astype(str)

df = df[['Nome', 'time', 'descricao', 'likes', 'comentarios', 'inter', 'tipo', 'link',
         'dia', 'hora', 'semana', 'Turno' ,'index', 'ID post', 'UNIDADE']]



with st.sidebar:
    st.markdown(html_title_sidebar, unsafe_allow_html=True)
    st.markdown("")

    opt = st.radio("Menu de navegação:", ("Monitor Manual", "Monitor Desenvolvido", "Monitor Individual"), index=0)

    if opt == "Monitor Manual":

        with st.expander("⚙️ Configurar Dados"):
            all_Nomes = df.Nome.unique().tolist()
            selected_Nomes = st.multiselect("Selecione as contas que deseja analisar:",
                                            options=all_Nomes, default=all_Nomes)

            all_tipos = df.tipo.unique().tolist()
            selected_tipos = st.multiselect("Selecione o tipo da publicação:",
                                            options=all_tipos, default=all_tipos)

            df["dia"] = pd.to_datetime(df["dia"]).dt.date
            data_start = df["dia"].unique().max()
            data_end = df["dia"].unique().min()
            date_min, date_max = st.date_input("Selecione o intervalo de datas:", (data_end, data_start))
            mask_data = (df['dia'] > date_min) & (df['dia'] <= date_max)

            slider1, slider2 = st.slider('Data Filtro Index', 0, len(df) - 1, [0, len(df) - 1], 1)
            mask_index = (df['index'] > slider1) & (df['index'] <= slider2)

        with st.expander("⚙️ Configurar Dashbords"):
            st.markdown("<h2 style='font-size:100%; text-align: left; color: #5B51D8;'" +
                        ">Gráfico de Barra - Análise Comparativa:</h2>",
                        unsafe_allow_html=True)

            df_x = df[['Nome', 'tipo', 'link', 'dia', 'hora', 'semana', 'Turno']]
            optionx = st.selectbox('Selecione coluna para o Eixo X:', df_x.columns.unique(), index=0)

            df_y = df[['likes', 'comentarios', 'inter', 'UNIDADE']]
            optiony = st.selectbox('Selecione coluna para o Eixo Y:', df_y.columns.unique(), index=0, key=10)
            st.markdown("")

            formato = st.radio("Selecione o formato para o Eixo Y:",
                               options=["Total de Atividades", "Média de Atividades", "Atividades por Publicação"])

            st.markdown("""---""")
            st.markdown("<h2 style='font-size:100%; text-align: left; color: #5B51D8;'" +
                        ">Gráfico de Linha - Análise Temporal:</h2>",
                        unsafe_allow_html=True)

            df_x_linha = df[['descricao', 'link', 'time', 'dia']]
            optionx_linha = st.selectbox('Selecione coluna para o Eixo X: - diferente',
                                         df_x_linha.columns.unique(), index=2, key=11)

            df_y_linha = df[['likes', 'comentarios', 'inter']]
            optiony_linha = st.selectbox('Selecione coluna para o Eixo Y:',
                                         df_y_linha.columns.unique(), index=0, key=12)

            st.markdown("""---""")
            st.markdown("<h2 style='font-size:100%; text-align: left; color: #5B51D8;'" +
                        ">Mapa de Calor - Análise por Matriz:</h2>",
                        unsafe_allow_html=True)

            formato_linha = st.radio("Selecione o formato para o Eixo Y:",
                                     options=["Total de Atividades", "Média de Atividades",
                                              "Atividades por Publicação"], key=13)

            df_heatmap = df[['likes', 'comentarios', 'inter']]
            option_heatmap = st.selectbox('Selecione a variável para o Mapa de Calor:',
                                          df_heatmap.columns.unique(), index=0)

            st.markdown("""---""")
            st.markdown("<h2 style='font-size:100%; text-align: left; color: #5B51D8;'" +
                        ">Nuvem de Palavras - Análise de Frequência:</h2>",
                        unsafe_allow_html=True)


    elif opt == "Monitor Desenvolvido":

        st.text("2")

    elif opt == "Monitor Individual":

        st.text("3")

    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")

    rodape1()


if opt == "Monitor Manual":
    topo1()
    st.markdown("""---""")

    with st.expander("👀 Sua primeira vez? Comece a explorar por aqui!"):

        st.markdown("O Data App é uma Aplicativo focado na análise e exploração de dados, está aplicacação "
                    "trabalha com dados das publicações dos maiores portais de noticias do Brasil, onde cada linha "
                    "da base de dados representa uma publicação.")
        st.markdown("Está primeira página é o Monitor Manual, seu objetivo é permitir ao usúario realizar a análise, exploração e "
                    "manipulação dos dados de entrada dos Gráficos e como esses Gráficos serão apresentados")

        st.markdown("<h2 style='font-size:150%; text-align: left; color: #5B51D8;'" +
                    ">Painel de Controle:</h2>",
                    unsafe_allow_html=True)
        st.markdown("O painel de controle, localizado na barra lateral, tem a função de armazar a nagevegação "
                    "entre paginas e as configurações, possibilitando ao usuário realizar aletrações nas visualizações "
                    "sem poluir a tela principal.")
        st.markdown("")

        col1, col2 = st.columns([1,1])
        with col1:
            st.markdown("<h2 style='font-size:150%; text-align: left; color: #5B51D8;'" +
                        ">Configurar entrada de Dados:</h2>",
                        unsafe_allow_html=True)
            st.markdown(
                "Localizado no Painel de Controle, as configurações de entrada de dados são o que alimenta os gráficos e tabela, "
                "que na pratica atua como filtros, onde o usuário pode selecionar informações bem espeficicas, como: "
                "mome do portal, tipo de publicação, intervalo de datas das publicações etc. ")
            st.markdown("")

        with col2:
            st.markdown("<h2 style='font-size:150%; text-align: left; color: #5B51D8;'" +
                        ">Configurar Gráficos:</h2>",
                        unsafe_allow_html=True)
            st.markdown("Também localizado no Painel de Controle, as configurações de Gráficos permitem ao usuário "
                        "selecionar quais informações deseja visualizar em cada tipo de gráfico, escolhendo entre "
                        "quais colunas serão Eixo X e Y, e como essas informações serão apresentadas, com valor Total "
                        "Média, unitario, etc.")
            st.markdown("")



        col1, col2 = st.columns([1,1])
        with col1:
            st.markdown("<h2 style='font-size:150%; text-align: left; color: #5B51D8;'" +
                        ">Tabela Interativa:</h2>",
                        unsafe_allow_html=True)
            st.markdown(
                "As tabelas neste App permitem ao usuário filtrar, ordenar e selecionar linhas e colunas especificas.")
        with col2:
            st.markdown("<h2 style='font-size:150%; text-align: left; color: #5B51D8;'" +
                        ">Gráfios Interativos:</h2>",
                        unsafe_allow_html=True)
            st.markdown("Os Gráficos apresentam informações complementares quando usuário colocar o mouse em cima dos eixos")
            st.markdown("")



        st.markdown("")

    inicio =  st.checkbox("Ativar Monitor Manual")

    if inicio:
        df = df[df.Nome.isin(selected_Nomes)]
        df = df[df.tipo.isin(selected_tipos)]
        df = df.loc[mask_data]
        df_select = df.loc[mask_index]

        st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                    ">Tabela Interativa: <i>" + str((len(df_select))) + "</i> publicações em análise</h1>",
                    unsafe_allow_html=True)

        selected_rows = folha_tabela(df_select)

        if len(selected_rows) != 0:
            fig1 = plot_bar(formato, selected_rows, optionx, optiony)
            st.plotly_chart(fig1, use_container_width=True)
            fig2 = plot_line(selected_rows, optionx_linha, optiony_linha)
            st.plotly_chart(fig2, use_container_width=True)
            fig3 = plot_hotmap(df_select, option_heatmap)
            st.plotly_chart(fig3, use_container_width=True)
            fig4 = plot_wordcoud(selected_rows)
            st.pyplot(fig4)

        if len(selected_rows) == 0:
            fig3A2 = plot_bar(formato, df_select, optionx, optiony)
            st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                        ">Análise de Comparativa - <i>" + optiony + "</i> por <i>" + optionx + "</i></h1>",
                        unsafe_allow_html=True)

            st.plotly_chart(fig3A2, use_container_width=True)

            st.text("")
            st.text("")

            fig2 = plot_line(df_select, optionx_linha, optiony_linha)
            st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                        ">Análise Tempotal - <i>" + optiony_linha + "</i> por <i>" + optionx_linha + "</i></h1>",
                        unsafe_allow_html=True)

            st.plotly_chart(fig2, use_container_width=True)
            st.text("")
            st.text("")

            try:
                fig3 = plot_hotmap(df_select, option_heatmap)
                st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                            ">Análise de <i>" + option_heatmap + "</i> por Turno e Dia da Semana</h1>",
                            unsafe_allow_html=True)

                st.plotly_chart(fig3, use_container_width=True)
            except:
                st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                            ">Análise de <i>" + option_heatmap + "</i> por Turno e Dia da Semana </h1>",
                            unsafe_allow_html=True)
                st.markdown("")
                st.warning(
                    'Os dodos selecionados são insuficientes par gerar o Mapa de calor, por favor adcione mais dados!',
                    icon="⚠️")
                st.text("")
                st.text("")

            st.text("")
            st.text("")

            fig4 = plot_wordcoud(df_select)
            st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                        ">Análise das palavras mais frequentes</h1>",
                        unsafe_allow_html=True)
            st.pyplot(fig4)
            st.text("")
            st.text("")

elif opt == "Monitor Desenvolvido":

    topo2()
    st.markdown("""---""")

    folha_posts(df)


st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")

rodape2()