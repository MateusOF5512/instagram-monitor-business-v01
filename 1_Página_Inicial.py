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
mask = (df['dia'] > '2022-09-20')
df = df.loc[mask]

df['link'] = 'www.instagram.com/p/' + df['shortcode'].astype(str)

df = df[['Nome', 'time', 'descricao', 'likes', 'comentarios', 'inter', 'tipo', 'link',
         'dia', 'hora', 'semana', 'Turno' ,'index', 'ID post', 'UNIDADE']]



with st.sidebar:
    st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8; padding: 0px 0px;'" +
                ">Painel de Controle</h1>",
                unsafe_allow_html=True)

    st.markdown("""---""")

    opt = st.radio("Navegação entre Páginas:", ("Monitor Personalizado", "Monitor Manual"),
                   index=0, help="Use para navegar entre as diferentes páginas do App")
    st.markdown("""---""")


    if opt == "Monitor Personalizado":

        with st.expander("⚙️ Configurar Dados"):
            all_Nomes_perz = df.Nome.unique().tolist()
            selected_Nome_perz = st.multiselect("Selecione as contas que deseja analisar:",
                                                options=all_Nomes_perz, default=all_Nomes_perz,
                                                help='Use para filtrar os nomes das contas no banco de dados.')

            all_tipos = df.tipo.unique().tolist()
            selected_tipos_perz = st.multiselect("Selecione os tipos das publicações:",
                                                 options=all_tipos, default=all_tipos,
                                                help='Use para filtrar os tipos de publicações no banco de dados.')

            df["dia_"] = pd.to_datetime(df["dia"]).dt.date
            data_start = df["dia_"].unique().max()
            data_end = df["dia_"].unique().min()
            date_min, date_max = st.date_input("Selecione o intervalo de datas:", (data_end, data_start),
                                                help='Use para filtrar o intervalo de datas no banco de dados.')
            mask_data_perz = (df['dia_'] > date_min) & (df['dia_'] <= date_max)

            all_semana = df.semana.unique().tolist()
            selected_semana_perz = st.multiselect("Selecione os dias da semana:",
                                                 options=all_semana, default=all_semana,
                                                 help='Use para filtrar os dias da semana no banco de dados.')

            hora_max = 0
            hora_min = 23
            slider1, slider2 = st.slider('Selecione o intervalo de horas:', hora_min, hora_max,
                                         [hora_min, hora_max], 1,
                                         help='Use para filtrar o intervalo de horas no banco de dados.')
            mask_hora_perz = (df['hora'] > slider1) & (df['hora'] <= slider2)



        with st.expander("⚙️ Configurar Dashbords"):
            st.markdown("<h2 style='font-size:100%; text-align: left; color: #5B51D8;'" +
                        ">Gráfico de Barra - Análise Comparativa:</h2>",
                        unsafe_allow_html=True)

            df_x = df[['Nome', 'tipo', 'link', 'dia', 'hora', 'semana', 'Turno']]
            optionx = st.selectbox('Selecione coluna para o Eixo X:', df_x.columns.unique(), index=0)

            df_y = df[['likes', 'comentarios', 'inter', 'UNIDADE']]
            optiony = st.selectbox('Selecione coluna para o Eixo Y:', df_y.columns.unique(), index=0, key=71)
            st.markdown("")

            formato = st.radio("Selecione o formato do Gráfico:",
                               options=["Total", "Média", "Por Publicação"], horizontal=True)

            st.markdown("""---""")
            st.markdown("<h2 style='font-size:100%; text-align: left; color: #5B51D8;'" +
                        ">Gráfico de Linha - Análise Temporal:</h2>",
                        unsafe_allow_html=True)

            df_x_linha = df[['time', 'dia', 'link']]
            optionx_linha = st.selectbox('Selecione coluna para o Eixo X: - diferente',
                                         df_x_linha.columns.unique(), index=1, key=72)

            df_y_linha = df[['likes', 'comentarios', 'inter', 'UNIDADE']]
            optiony_linha = st.selectbox('Selecione coluna para o Eixo Y:',
                                         df_y_linha.columns.unique(), index=0, key=73)

            formato_linha = st.radio("Selecione o formato do Gráfico:",
                                     options=["Total", "Média"], key=74, horizontal=True)

            st.markdown("""---""")
            st.markdown("<h2 style='font-size:100%; text-align: left; color: #5B51D8;'" +
                        ">Mapa de Calor - Análise por Matriz:</h2>",
                        unsafe_allow_html=True)


            df_heatmap = df[['likes', 'comentarios', 'inter',  'UNIDADE']]
            option_heatmap = st.selectbox('Selecione a variável do Gráfico:',
                                          df_heatmap.columns.unique(), index=0)

            formato_map = st.radio("Selecione o formato do Gráfico:",
                                     options=["Total", "Média"], key=14, horizontal=True)

            st.markdown("""---""")
            st.markdown("<h2 style='font-size:100%; text-align: left; color: #5B51D8;'" +
                        ">Nuvem de Palavras - Análise de Frequência:</h2>",
                        unsafe_allow_html=True)



    if opt == "Monitor Manual":
        with st.expander("⚙️ Configurar Dados"):
            all_Nomes = df.Nome.unique().tolist()
            selected_Nomes = st.multiselect("Selecione as contas que deseja analisar:",
                                            options=all_Nomes, default=all_Nomes)

            all_tipos = df.tipo.unique().tolist()
            selected_tipos = st.multiselect("Selecione o tipo da publicação:",
                                            options=all_tipos, default=all_tipos)

            df["dia_"] = pd.to_datetime(df["dia"]).dt.date
            data_start = df["dia_"].unique().max()
            data_end = df["dia_"].unique().min()
            date_min, date_max = st.date_input("Selecione o intervalo de datas:", (data_end, data_start))
            mask_data = (df['dia_'] > date_min) & (df['dia_'] <= date_max)

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

            formato = st.radio("Selecione o formato do Gráfico:",
                               options=["Total", "Média", "Por Publicação"], horizontal=True)

            st.markdown("""---""")
            st.markdown("<h2 style='font-size:100%; text-align: left; color: #5B51D8;'" +
                        ">Gráfico de Linha - Análise Temporal:</h2>",
                        unsafe_allow_html=True)

            df_x_linha = df[['time', 'dia', 'link']]
            optionx_linha = st.selectbox('Selecione coluna para o Eixo X: - diferente',
                                         df_x_linha.columns.unique(), index=1, key=11)

            df_y_linha = df[['likes', 'comentarios', 'inter', 'UNIDADE']]
            optiony_linha = st.selectbox('Selecione coluna para o Eixo Y:',
                                         df_y_linha.columns.unique(), index=0, key=12)

            formato_linha = st.radio("Selecione o formato do Gráfico:",
                                     options=["Total", "Média"], key=13, horizontal=True)

            st.markdown("""---""")
            st.markdown("<h2 style='font-size:100%; text-align: left; color: #5B51D8;'" +
                        ">Mapa de Calor - Análise por Matriz:</h2>",
                        unsafe_allow_html=True)


            df_heatmap = df[['likes', 'comentarios', 'inter',  'UNIDADE']]
            option_heatmap = st.selectbox('Selecione a variável do Gráfico:',
                                          df_heatmap.columns.unique(), index=0)

            formato_map = st.radio("Selecione o formato do Gráfico:",
                                     options=["Total", "Média"], key=14, horizontal=True)

            st.markdown("""---""")
            st.markdown("<h2 style='font-size:100%; text-align: left; color: #5B51D8;'" +
                        ">Nuvem de Palavras - Análise de Frequência:</h2>",
                        unsafe_allow_html=True)


    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")


    rodape1()


if opt == "Monitor Personalizado":

    st.markdown("<h1 style='font-size:220%; text-align: center; color: #5B51D8; padding: 0px 20px;'" +
                ">Data App - Instagram Monitore</h1>",
                unsafe_allow_html=True)
    st.markdown("<h2 style='font-size:150%; text-align: center; color: #5B51D8; padding: 5px 0px;'" +
                ">Publicações dos maiores Instagrans de Notícias do Brasil</h2>",
                unsafe_allow_html=True)
    st.markdown("""---""")


    df = df[df.Nome.isin(selected_Nome_perz)]
    df = df[df.tipo.isin(selected_tipos_perz)]
    df = df[df.semana.isin(selected_semana_perz)]
    df = df.loc[mask_data_perz]
    df_select = df.loc[mask_hora_perz]


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

    inicio_personalizado = st.checkbox("Ativar Monitor Personalizado")

    if inicio_personalizado:

        st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                    ">Tabela Interativa: <i>" + str((len(df_select))) + "</i> publicações em análise</h1>",
                    unsafe_allow_html=True)

        selected_rows = folha_tabela(df_select)

        if len(selected_rows) != 0:
            folha_posts(selected_rows)

        elif len(selected_rows) == 0:
            folha_posts(df_select)



###########################################################################################

elif opt == "Monitor Manual":
    #topo1()
    st.markdown("<h1 style='font-size:220%; text-align: center; color: #5B51D8; padding: 0px 20px;'" +
                    ">Data App - Instagram Monitore</h1>",
                    unsafe_allow_html=True)
    st.markdown("<h2 style='font-size:150%; text-align: center; color: #5B51D8; padding: 5px 0px;'" +
                ">Publicações dos maiores Instagrans de Notícias do Brasil</h2>",
                unsafe_allow_html=True)
    st.markdown("""---""")
    #st.markdown("")

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

    inicio_manual = st.checkbox("Ativar Monitor Manual")
    if inicio_manual:

        st.markdown("")


        df = df[df.Nome.isin(selected_Nomes)]
        df = df[df.tipo.isin(selected_tipos)]
        df = df.loc[mask_data]
        df_select = df.loc[mask_index]

        st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                    ">Tabela Interativa: <i>" + str((len(df_select))) + "</i> publicações em análise</h1>",
                    unsafe_allow_html=True)

        selected_rows = folha_tabela(df_select)

        if len(selected_rows) != 0:

            fig3A2 = plot_bar(formato, selected_rows, optionx, optiony)
            st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                        "><i>" + formato + "</i> de <i>" + optiony + "</i> por <i>" + optionx + "</i> - Análise de Comparativa</h1>",
                        unsafe_allow_html=True)

            st.plotly_chart(fig3A2, use_container_width=True)

            with st.expander("🔎️   Dados - Análise Comparativa"):
                col1, col2 = st.columns([1, 1])
                df_sum = selected_rows.groupby([optionx])[optiony].agg('sum').reset_index().sort_values(optionx,
                                                                                                    ascending=True)

                checkdf = st.checkbox('Visualizar Dados', key=50)
                if checkdf:
                    simple_aggrid(df_sum)

                df_sum = df_sum.to_csv(index=False).encode('utf-8')
                st.download_button(label="Download Dados", data=df_sum,
                                   file_name="DataApp_Analise_Comparativa.csv", mime='text/csv')

            st.markdown("""---""")

            st.text("")
            st.text("")

            fig2 = plot_line(selected_rows, optionx_linha, optiony_linha, formato_linha)
            st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                        "><i>" + formato_linha + "</i> de <i>" + optiony_linha + "</i> por <i>" + optionx_linha + "</i> - Análise Tempotal</h1>",
                        unsafe_allow_html=True)

            st.plotly_chart(fig2, use_container_width=True)

            with st.expander("🔎️   Dados - Análise Tempotal"):
                df_temp = selected_rows.groupby([optionx_linha]).agg('sum').reset_index()
                df_temp = df_temp[[optionx_linha, optiony_linha]]

                checkdf = st.checkbox('Visualizar Dados', key=52)
                if checkdf:
                    simple_aggrid(df_temp)

                df_temp = df_temp.to_csv(index=False).encode('utf-8')
                st.download_button(label="Download Dados", data=df_temp,
                                   file_name="DataApp_Analise_Temporal.csv", mime='text/csv')

            st.markdown("""---""")

            st.text("")
            st.text("")

            try:
                fig3 = plot_hotmap(selected_rows, option_heatmap, formato_map)
                st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                            "><i>" + formato_map + "</i> de <i>" + option_heatmap + "</i> por Turno e Dia da Semana</h1>",
                            unsafe_allow_html=True)

                st.plotly_chart(fig3, use_container_width=True)

                with st.expander("🔎️  Dados - Análise por Turno e Dia da Semana"):
                    col1, col2 = st.columns([1, 1])
                    df_map = selected_rows.groupby(['semana', 'Turno']).agg('sum').reset_index()
                    df_map = df_map[['semana', 'Turno', option_heatmap]]

                    checkdf = st.checkbox('Visualizar Dados', key=53)
                    if checkdf:
                        simple_aggrid(df_map)

                    df_map = df_map.to_csv(index=False).encode('utf-8')
                    st.download_button(label="Download Dados", data=df_map,
                                       file_name="DataApp_Analise_Turno_Semana.csv", mime='text/csv')

                st.markdown("""---""")

            except:
                st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                            ">Análise de <i>" + option_heatmap + "</i> por Turno e Dia da Semana </h1>",
                            unsafe_allow_html=True)
                st.markdown("")
                st.warning(
                    'Os dodos selecionados são insuficientes par gerar o Mapa de calor, por favor adcione mais dados!',
                    icon="⚠️")

                with st.expander("🔎️  Dados - Análise por Turno e Dia da Semana"):
                    col1, col2 = st.columns([1, 1])
                    df_map = selected_rows.groupby(['semana', 'Turno']).agg('sum').reset_index()
                    df_map = df_map[['semana', 'Turno', option_heatmap]]

                    checkdf = st.checkbox('Visualizar Dados', key=53)
                    if checkdf:
                        simple_aggrid(df_map)

                    df_map = df_map.to_csv(index=False).encode('utf-8')
                    st.download_button(label="Download Dados", data=df_map,
                                       file_name="DataApp_Analise_Turno_Semana.csv", mime='text/csv')

            st.markdown("""---""")

            st.text("")
            st.text("")

            fig4 = plot_wordcoud(selected_rows)
            st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                        ">Análise das palavras mais frequentes</h1>",
                        unsafe_allow_html=True)
            st.pyplot(fig4)

            with st.expander("🔎️   Dados - Palavras Frequêntes"):
                df_word = selected_rows[["descricao"]]

                checkdf = st.checkbox('Visualizar Dados', key=54)
                if checkdf:
                    simple_aggrid(df_word)

                df_word = df_word.to_csv(index=False).encode('utf-8')
                st.download_button(label="Download Dados", data=df_word,
                                   file_name="DataApp_Analise_Temporal.csv", mime='text/csv')

            st.markdown("""---""")
            st.text("")
            st.text("")









        if len(selected_rows) == 0:
            fig3A2 = plot_bar(formato, df_select, optionx, optiony)
            st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                        "><i>"+formato+"</i> de <i>" + optiony + "</i> por <i>" + optionx + "</i> - Análise de Comparativa</h1>",
                        unsafe_allow_html=True)

            st.plotly_chart(fig3A2, use_container_width=True)

            with st.expander("🔎️   Dados - Análise Comparativa"):
                col1, col2 = st.columns([1, 1])
                df_sum = df_select.groupby([optionx])[optiony].agg('sum').reset_index().sort_values(optionx,
                                                                                                    ascending=True)

                checkdf = st.checkbox('Visualizar Dados', key=50)
                if checkdf:
                    simple_aggrid(df_sum)

                df_sum = df_sum.to_csv(index=False).encode('utf-8')
                st.download_button(label="Download Dados", data=df_sum,
                                           file_name="DataApp_Analise_Comparativa.csv", mime='text/csv')

            st.markdown("""---""")

            st.text("")
            st.text("")

            fig2 = plot_line(df_select, optionx_linha, optiony_linha, formato_linha)
            st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                        "><i>"+formato_linha+"</i> de <i>"+optiony_linha+"</i> por <i>"+optionx_linha+"</i> - Análise Tempotal</h1>",
                        unsafe_allow_html=True)

            st.plotly_chart(fig2, use_container_width=True)

            with st.expander("🔎️   Dados - Análise Tempotal"):
                df_temp = df_select.groupby([optionx_linha]).agg('sum').reset_index()
                df_temp = df_temp[[optionx_linha, optiony_linha]]

                checkdf = st.checkbox('Visualizar Dados', key=52)
                if checkdf:
                    simple_aggrid(df_temp)

                df_temp = df_temp.to_csv(index=False).encode('utf-8')
                st.download_button(label="Download Dados", data=df_temp,
                                       file_name="DataApp_Analise_Temporal.csv", mime='text/csv')

            st.markdown("""---""")

            st.text("")
            st.text("")

            try:
                fig3 = plot_hotmap(df_select, option_heatmap, formato_map)
                st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                            "><i>"+formato_map+"</i> de <i>"+option_heatmap+"</i> por Turno e Dia da Semana</h1>",
                            unsafe_allow_html=True)

                st.plotly_chart(fig3, use_container_width=True)

                with st.expander("🔎️  Dados - Análise por Turno e Dia da Semana"):
                    col1, col2 = st.columns([1, 1])
                    df_map = df_select.groupby(['semana', 'Turno']).agg('sum').reset_index()
                    df_map = df_map[['semana', 'Turno', option_heatmap]]

                    checkdf = st.checkbox('Visualizar Dados', key=53)
                    if checkdf:
                        simple_aggrid(df_map)

                    df_map = df_map.to_csv(index=False).encode('utf-8')
                    st.download_button(label="Download Dados", data=df_map,
                                           file_name="DataApp_Analise_Turno_Semana.csv", mime='text/csv')

                st.markdown("""---""")

            except:
                st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                            ">Análise de <i>" + option_heatmap + "</i> por Turno e Dia da Semana </h1>",
                            unsafe_allow_html=True)
                st.markdown("")
                st.warning(
                    'Os dodos selecionados são insuficientes par gerar o Mapa de calor, por favor adcione mais dados!',
                    icon="⚠️")

                with st.expander("🔎️  Dados - Análise por Turno e Dia da Semana"):
                    col1, col2 = st.columns([1, 1])
                    df_map = df_select.groupby(['semana', 'Turno']).agg('sum').reset_index()
                    df_map = df_map[['semana', 'Turno', option_heatmap]]

                    checkdf = st.checkbox('Visualizar Dados', key=53)
                    if checkdf:
                        simple_aggrid(df_map)

                    df_map = df_map.to_csv(index=False).encode('utf-8')
                    st.download_button(label="Download Dados", data=df_map,
                                           file_name="DataApp_Analise_Turno_Semana.csv", mime='text/csv')

            st.markdown("""---""")

            st.text("")
            st.text("")

            fig4 = plot_wordcoud(df_select)
            st.markdown("<h1 style='font-size:150%; text-align: center; color: #5B51D8;'" +
                        ">Análise das palavras mais frequentes</h1>",
                        unsafe_allow_html=True)
            st.pyplot(fig4)

            with st.expander("🔎️   Dados - Palavras Frequêntes"):
                df_word = df_select[["descricao"]]

                checkdf = st.checkbox('Visualizar Dados', key=54)
                if checkdf:
                    simple_aggrid(df_word)

                df_word = df_word.to_csv(index=False).encode('utf-8')
                st.download_button(label="Download Dados", data=df_word,
                                       file_name="DataApp_Analise_Temporal.csv", mime='text/csv')

            st.markdown("""---""")
            st.text("")
            st.text("")





st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")

rodape2()