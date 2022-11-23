# Importação de Bibliotecas:

from outros.variaveis_folha import *
from plots.plots_choquei import *
import streamlit as st

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode


## - Topo e Rodapé da Aplicação:
def topo():
    st.markdown(html_title, unsafe_allow_html=True) #Explorador de Dados Abertos
    st.markdown(""" <style>
        footer {visibility: hidden;}
        </style> """, unsafe_allow_html=True)
    return None

def rodape():
    st.markdown(html_rodape, unsafe_allow_html=True) # ---- by: mateus
    return None

config={"displayModeBar": True,
        "displaylogo": False,
        'modeBarButtonsToRemove': ['zoom2d', 'toggleSpikelines',
                                   'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                   'hoverClosestCartesian', 'hoverCompareCartesian']}

def folha_posts(df):
    st.text("")
    st.text("")
    st.markdown(html_header_10, unsafe_allow_html=True)  # 2 - Características da População Vacinada
    st.markdown('''---''')
    st.text("")

    col1A, col2A, col3A, col4A, col5A = st.columns([50, 520, 60, 520, 50])
    with col1A:
        st.text("")
    with col2A:
        st.markdown(html_card_header_AA1, unsafe_allow_html=True)  # Descrição Inicial
        st.plotly_chart(figA1, use_container_width=True, config=config)  # GRÁFICO DE BARRA HORIZONTAL
        st.plotly_chart(figA2, use_container_width=True, config=config)  # GRÁFICO DE BARRA HORIZONTAL
        st.plotly_chart(figA3, use_container_width=True, config=config)  # GRÁFICO DE BARRA HORIZONTAL
    with col3A:
        st.text("")
    with col4A:
        st.markdown(html_card_header_ABB, unsafe_allow_html=True)  # Links importantes
        st.plotly_chart(figA4, use_container_width=True, config=config)  # GRÁFICO DE BARRA HORIZONTAL
    with col5A:
        st.text("")

    col1, col2, col3, col4, col5 = st.columns([50, 520, 60, 520, 50])
    with col1:
        st.text("")
    with col2:
        st.markdown(html_card_header_AA1, unsafe_allow_html=True)  # Descrição Inicial
        st.plotly_chart(figB1, use_container_width=True, config=config)  # GRÁFICO DE BARRA HORIZONTAL
    with col3:
        st.text("")
    with col4:
        st.markdown(html_card_header_ABB, unsafe_allow_html=True)  # Links importantes
        st.plotly_chart(figB2, use_container_width=True, config=config)  # GRÁFICO DE BARRA HORIZONTAL
    with col5:
        st.text("")

    col1, col2, col3, col4, col5 = st.columns([50, 520, 60, 520, 50])
    with col1:
        st.text("")
    with col2:
        st.markdown(html_card_header_AA1, unsafe_allow_html=True)  # Descrição Inicial
        st.plotly_chart(figC1, use_container_width=True, config=config)  # GRÁFICO DE BARRA HORIZONTAL
    with col3:
        st.text("")
    with col4:
        st.markdown(html_card_header_ABB, unsafe_allow_html=True)  # Links importantes
        st.plotly_chart(figC2, use_container_width=True, config=config)  # GRÁFICO DE BARRA HORIZONTAL
    with col5:
        st.text("")

    col1, col2, col3, col4, col5 = st.columns([50, 520, 60, 520, 50])
    with col1:
        st.text("")
    with col2:
        df_ = df[['descricao','tipo', 'likes', 'comentarios', 'inter','time', 'index', 'shortcode']]

        st.markdown(html_card_header_AA1, unsafe_allow_html=True)  # Descrição Inicial

        gd = GridOptionsBuilder.from_dataframe(df_)
        gd.configure_pagination(enabled=True)
        gd.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=True)
        gd.configure_side_bar()
        gridoptions = gd.build()

        AgGrid(df_, gridOptions=gridoptions, enable_enterprise_modules=False, height=250, width='100%')
    with col3:
        st.text("")
    with col4:
        st.markdown(html_card_header_ABB, unsafe_allow_html=True)  # Links importantes
        st.pyplot(figD1)  # GRÁFICO DE BARRA HORIZONTAL
    with col5:
        st.text("")

    st.write("")
    return None


def folha_tabela(df):
    col1, col2, col3 = st.columns([50, 1100, 50])
    with col1:
        st.text("")
    with col2:
        st.markdown(html_card_header_3A1, unsafe_allow_html=True)

        gd = GridOptionsBuilder.from_dataframe(df)
        gd.configure_pagination(enabled=False)
        gd.configure_side_bar()
        gd.configure_default_column(groupable=True, value=True, enableRowGroup=True,
                                    aggFunc="sum", editable=True)
        gd.configure_selection(use_checkbox=True, selection_mode='multiple')
        gridoptions = gd.build()
        df_grid = AgGrid(df, gridOptions=gridoptions, enable_enterprise_modules=False,
                         update_mode=GridUpdateMode.SELECTION_CHANGED, height=350, width='100%')
        selected_rows = df_grid["selected_rows"]
        selected_rows = pd.DataFrame(selected_rows)

    with col3:
        st.text("")

    if len(selected_rows) != 0:
        figB4 = go.Figure()
        figB4.add_trace(go.Bar(
            name='Comentários', x=selected_rows['Ano'].sum(), y=selected_rows['inscritos_vestibular'].sum(),
            hovertemplate="</br><b>Comentários:</b> %{y:.2f}",
            textposition='none', marker_color=('#4B0082')
        ))
        st.plotly_chart(figB4)





    return None



def folha_tabela(df):
    col1, col2, col3 = st.columns([50, 1100, 50])
    with col1:
        st.text("")
    with col2:
        st.markdown(html_card_header_3A1, unsafe_allow_html=True)

        gd = GridOptionsBuilder.from_dataframe(df)
        gd.configure_pagination(enabled=False)
        gd.configure_side_bar()
        gd.configure_default_column(groupable=True, value=True, enableRowGroup=True,
                                    aggFunc="sum", editable=True)
        gd.configure_selection(use_checkbox=True, selection_mode='multiple')
        gridoptions = gd.build()
        df_grid = AgGrid(df, gridOptions=gridoptions, enable_enterprise_modules=False,
                         update_mode=GridUpdateMode.SELECTION_CHANGED, height=350, width='100%')
        selected_rows = df_grid["selected_rows"]
        selected_rows = pd.DataFrame(selected_rows)

        return selected_rows