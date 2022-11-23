# BIBLIOTECAS USADAS

import streamlit as st
from PIL import Image

im = Image.open("instagram.png")
st.set_page_config(page_title="Instagram Monitor", page_icon=im, layout="wide")
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

from layout.layout_choquei import *
from plots.plots_choquei import *
from plots.plots_folha import *
from outros.variaveis_folha import *


df = get_data(path_todos)
df = tratamento_dados2(df)


df = df[['Nome', 'descricao', 'likes', 'comentarios', 'inter', 'tipo',
         'shortcode', 'time', 'dia', 'hora', 'semana', 'Turno']]

# APLICAÇÃO
topo()
st.markdown("""---""")

selected_rows = folha_tabela(df)

col1A, col2A, col3A = st.columns([500, 25, 500,])
with col1A:
    optionx = st.selectbox('Selecione coluna para o eixo X:', df.columns.unique(), index=0)
with col2A:
    st.text("")
with col3A:
    optiony = st.selectbox('Selecione coluna para o eixo Y:', df.columns.unique(), index=4)

if len(selected_rows) != 0:
    x = df[optionx]
    y = df[optiony]
    fig3A1 = go.Figure()
    fig3A1.add_trace(go.Bar(
        name='Comentários', x=x, y=y,
        hovertemplate="%{y:.0f}",
        textposition='none', marker_color=('#4B0082')))

    fig3A1.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=11, orientation="h", yanchor="top", y=1.20, xanchor="center", x=0.5),
        height=300, barmode='stack', margin=dict(l=1, r=1, b=1, t=1), autosize=True, hovermode="x")
    fig3A1.update_xaxes(
        title_text=optionx, title_font=dict(family='Sans-serif', size=14),
        tickfont=dict(family='Sans-serif', size=12), showgrid=False)
    fig3A1.update_yaxes(
        title_text=optiony, title_font=dict(family='Sans-serif', size=14),
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    st.plotly_chart(fig3A1, use_container_width=True)

if len(selected_rows) == 0:
    x = df[optionx]
    y = df[optiony]

    fig3A1 = go.Figure()
    fig3A1.add_trace(go.Bar(
        name='Comentários', x=x, y=y,
        hovertemplate="%{y:.0f}",
        textposition='none', marker_color=('#4B0082')))

    fig3A1.update_xaxes(
        title_text=optionx, title_font=dict(family='Sans-serif', size=14),
        tickfont=dict(family='Sans-serif', size=12), showgrid=False)
    fig3A1.update_yaxes(
        title_text=optiony, title_font=dict(family='Sans-serif', size=14),
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    st.plotly_chart(fig3A1, use_container_width=True)


