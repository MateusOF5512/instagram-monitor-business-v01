import streamlit as st
from layout.layout_uol import *
from plots.plots_uol import *
from outros.variaveis_folha import *

df = get_data(path_uol)
df = tratamento_dados2(df)

tab1, tab2, tab3 = st.tabs(["😍 Monitor de Publicações", "💬 Monitor de Comentários", "🧮 Tabela Interativa"])
with tab1:
    folha_posts(df)
with tab2:
    st.markdown('teste 1')
with tab3:
    selected_rows = folha_tabela(df)

    optionx = st.selectbox(
        'Selecione coluna para o eixo X:', df.columns.unique(), index=1)

    optiony = st.selectbox(
        'Selecione coluna para o eixo Y:', df.columns.unique(), index=3)

    if len(selected_rows) != 0:
        x = df[optionx]
        y = df[optiony]
        fig3A1 = go.Figure()
        fig3A1.add_trace(go.Bar(
            name='Comentários', x=x, y=y,
            hovertemplate="</br><b>Comentários:</b> %{y:.2f}",
            textposition='none', marker_color=('#4B0082')))

        st.plotly_chart(fig3A1, use_container_width=True)
    if len(selected_rows) == 0:
        x = df[optionx]
        y = df[optiony]

        fig3A1 = go.Figure()
        fig3A1.add_trace(go.Bar(
            name='Comentários', x=x, y=y,
            hovertemplate="</br><b>Comentários:</b> %{y:.2f}",
            textposition='none', marker_color=('#4B0082')))

        st.plotly_chart(fig3A1, use_container_width=True)





