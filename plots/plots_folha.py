import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import numpy as np
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode


from outros.variaveis_folha import *

# CARREGANDO OS DADOS:
@st.cache(allow_output_mutation=True)
def get_data( path_posts ):
    df = pd.read_csv( path_posts )
    return df

def get_data_comentarios( path_comentarios ):
    df_com = pd.read_csv( path_comentarios )
    return df_com


def tratamento_dados2(df):
    df['conta'] = np.where(df['likes'] == 2, 0, 1)
    df.rename(columns={'Unnamed: 0': 'index'}, inplace=True)
    conditions = [
        (df['hora'] >= 6) & (df['hora'] <= 12),
        (df['hora'] >= 12) & (df['hora'] <= 18),
        (df['hora'] >= 18) & (df['hora'] <= 24),
        (df['hora'] >= 0) & (df['hora'] <= 6)]
    values = ['Manhã', 'Tarde', 'Noite', 'Madrugada']
    df['Turno'] = np.select(conditions, values)

    return df


df = get_data(path_posts)
df = tratamento_dados2(df)

im1 = Image.open("publicacao.jpeg")
im2 = Image.open("like.png")
im3 = Image.open("comentario.png")

### GRAFICO INDICADOR - MÉTRICAS GLOBAIS, LIKES E COMENTÁRIOS
# DADOS DE ENTRADA:
df_metricas = df.describe().reset_index()
# GRAFICO 1:
num_publi = 150
seguidores = 10000
senguindo = 1089
#GRÁFICO 2:
num_post_like = df_metricas["likes"].iloc[0]
soma_post_like = int(df['likes'].sum())
media_post_like = df_metricas["likes"].iloc[1]
min_post_like = df_metricas["likes"].iloc[3]
max_post_like = df_metricas["likes"].iloc[7]
#GRÁFICO 3:
soma_post_comments = int(df['comentarios'].sum())
media_post_comments = df_metricas["comentarios"].iloc[1]
min_post_comments = df_metricas["comentarios"].iloc[3]
max_post_comments = df_metricas["comentarios"].iloc[7]

# CONFIGURANDO GRAFICO INDICADOR 1 -  METRICAS GLOBAIS
figA1 = go.Figure()
figA1.add_trace(go.Indicator(
    mode="number",
    number_font_size=30,
    number_font_color="#5B51D8",
    value=num_publi,
    title={"text": "<span style='font-size:14px;color:black'>Publicações:</span>"},
    domain = {'y': [0, 1], 'x': [0.25, 0.5]}))
figA1.add_trace(go.Indicator(
    mode="number",
    number_font_size=30,
    number_font_color="#5B51D8",
    value=seguidores,
    title={"text": "<span style='font-size:14px;color:black'>Seguidores:</span>"},
    domain = {'y': [0, 1], 'x': [0.5, 0.75]}))
figA1.add_trace(go.Indicator(
    mode="number",
    number_font_size=30,
    number_font_color="#5B51D8",
    value=senguindo,
    title={"text": "<span style='font-size:14px;color:black'>Seguindo:</span>"},
    domain = {'y': [0, 1], 'x': [0.75, 1]}))
figA1.update_layout(
    paper_bgcolor="#F8F8FF", height=70, margin=dict(l=10, r=10, b=10, t=40),
    grid={'rows': 1, 'columns': 3})

figA1.add_layout_image(dict(source=im1, xref="paper", yref="paper", x=0.05, y=1, xanchor='left', yanchor='middle',
                          sizex=2, sizey=2))

# CONFIGURANDO GRAFICO INDICADOR 2 -  METRICAS LIKES
figA2 = go.Figure()
figA2.add_trace(go.Indicator(
    mode="number",
    number_font_size=20,
    number_font_color="#FD1D1D",
    value=soma_post_like,
    title={"text": "<span style='font-size:14px;color:black'>Total:</span>"},
    domain = {'y': [0, 1], 'x': [0.2, 0.4]}))
figA2.add_trace(go.Indicator(
    mode="number",
    number_font_size=20,
    number_font_color="#FD1D1D",
    value=media_post_like,
    title={"text": "<span style='font-size:14px;color:black'>Média:</span>"},
    domain = {'y': [0, 1], 'x': [0.4, 0.6]}))
figA2.add_trace(go.Indicator(
    mode="number",
    number_font_size=20,
    number_font_color="#FD1D1D",
    value=min_post_like,
    title={"text": "<span style='font-size:14px;color:black'>Mínimo:</span>"},
    domain = {'y': [0, 1], 'x': [0.6, 0.8]}))
figA2.add_trace(go.Indicator(
    mode="number",
    number_font_size=20,
    number_font_color="#FD1D1D",
    value=max_post_like,
    title={"text": "<span style='font-size:14px;color:black'>Máximo:</span>"},
    domain = {'y': [0, 1], 'x': [0.8, 1]}))
figA2.update_layout(
    paper_bgcolor="#F8F8FF", height=70, margin=dict(l=1, r=1, b=1, t=30),
    grid={'rows': 1, 'columns': 4})

figA2.add_layout_image(dict(source=im2, xref="paper", yref="paper", x=0.05, y=0.75, xanchor='left', yanchor='middle',
                          sizex=1.4, sizey=1.4))

# CONFIGURANDO GRAFICO INDICADOR 3 -  METRICAS COMENTÁRIOS
figA3 = go.Figure()
figA3.add_trace(go.Indicator(
    mode="number",
    number_font_size=20,
    number_font_color="#F56040",
    value=soma_post_comments,
    title={"text": "<span style='font-size:14px;color:black'>Total:</span>"},
    domain = {'y': [0, 1], 'x': [0.2, 0.4]}))
figA3.add_trace(go.Indicator(
    mode="number",
    number_font_size=20,
    number_font_color="#F56040",
    value=media_post_comments,
    title={"text": "<span style='font-size:14px;color:black'>Média:</span>"},
    domain = {'y': [0, 1], 'x': [0.4, 0.6]}))
figA3.add_trace(go.Indicator(
    mode="number",
    number_font_size=20,
    number_font_color="#F56040",
    value=min_post_comments,
    title={"text": "<span style='font-size:14px;color:black'>Mínimo:</span>"},
    domain = {'y': [0, 1], 'x': [0.6, 0.8]}))
figA3.add_trace(go.Indicator(
    mode="number",
    number_font_size=20,
    number_font_color="#F56040",
    value=max_post_comments,
    title={"text": "<span style='font-size:14px;color:black'>Máximo:</span>"},
    domain = {'y': [0, 1], 'x': [0.8, 1]}))
figA3.update_layout(
    paper_bgcolor="#F8F8FF", height=70, margin=dict(l=1, r=1, b=0, t=30),
    grid={'rows': 1, 'columns': 4})

figA3.add_layout_image(dict(source=im3, xref="paper", yref="paper", x=0.01, y=0.75, xanchor='left', yanchor='middle',
                          sizex=1.3, sizey=1.3))


### GRAFICO 2 - PIZZA -
im1 = Image.open("publicacao.jpeg")
im2 = Image.open("like.png")
im3 = Image.open("comentario.png")

df_type = df.groupby('tipo').agg('sum')
IMAGEM = df_type["conta"].iloc[1]
VIDEO = df_type["conta"].iloc[2]
COLECAO = df_type["conta"].iloc[0]

IMAGEM_LIKES = df_type["likes"].iloc[1]
VIDEO_LIKES = df_type["likes"].iloc[2]
COLECAO_LIKES = df_type["likes"].iloc[0]

IMAGEM_COMENTARIOS = df_type["comentarios"].iloc[1]
VIDEO_COMENTARIOS = df_type["comentarios"].iloc[2]
COLECAO_COMENTARIOS = df_type["comentarios"].iloc[0]

labels = ['Imagem', "Coleção", 'Vídeo']
colors = ['#E1306C', '#C13584', '#833AB4']
figA4 = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]],
                      subplot_titles=['Publicações', 'Likes', 'Comentários', ])

figA4.add_trace(go.Pie(labels=labels, name="Publicações",
                       values=[IMAGEM, COLECAO, VIDEO],
                       textinfo='none', showlegend=True,
                       domain={'y': [0, 1], 'x': [0, 0.3]},
                       marker=dict(colors=colors, line=dict(color='#000010', width=2))))

figA4.add_trace(go.Pie(labels=labels, name="Likes",
                       values=[IMAGEM_LIKES, COLECAO_LIKES, VIDEO_LIKES],
                       textinfo='none', showlegend=True,
                       domain={'y': [0, 1], 'x': [0.35, 0.65]},
                       marker=dict(colors=colors, line=dict(color='#000010', width=2))))
figA4.add_trace(go.Pie(labels=labels, name="Comentários",
                       values=[IMAGEM_COMENTARIOS, COLECAO_COMENTARIOS, VIDEO_COMENTARIOS],
                       textinfo='none', showlegend=True,
                       domain={'y': [0, 1], 'x': [0.7, 1]},
                       marker=dict(colors=colors, line=dict(color='#000010', width=2))))

figA4.update_traces(hole=.8, hoverinfo="label+name+percent+value",
                    hovertemplate="</br><b>Publicação:</b> %{label} " +
                                  "</br><b>Quantidade:</b>  %{value}" +
                                  "</br><b>Proporção:</b>  %{percent}")
figA4.update_layout(autosize=True,
                   height=270, margin=dict(l=10, r=10, b=2, t=40),
                   legend=dict(font_size=14, orientation="h", yanchor="top",
                               y=-0.05, xanchor="center", x=0.5),
                   paper_bgcolor="#F8F8FF", font={'size': 20})

figA4.add_layout_image(dict(source=im1, xref="paper", yref="paper", x=0.095, y=0.65,
                          sizex=0.3, sizey=0.3))
figA4.add_layout_image(dict(source=im2, xref="paper", yref="paper", x=0.445, y=0.65,
                          sizex=0.3, sizey=0.3))
figA4.add_layout_image(dict(source=im3, xref="paper", yref="paper", x=0.75, y=0.65,
                          sizex=0.3, sizey=0.3))

##############################################################################################################
###############################################################################################################

### GRAFICO 5 - BARRA -
df_week = df.groupby('semana').agg('mean')
df_week_soma = df.groupby('semana').agg('sum')

values = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
y_like = [df_week['likes'][0], df_week['likes'][1], df_week['likes'][2], df_week['likes'][3],
          df_week['likes'][4], df_week['likes'][5], df_week['likes'][6]]
y_comments = [df_week['comentarios'][0], df_week['comentarios'][1], df_week['comentarios'][2], df_week['comentarios'][3],
              df_week['comentarios'][4], df_week['comentarios'][5], df_week['comentarios'][6]]
y_num = [df_week_soma['conta'][0], df_week_soma['conta'][1], df_week_soma['conta'][2], df_week_soma['conta'][3],
         df_week_soma['conta'][4], df_week_soma['conta'][5], df_week_soma['conta'][6]]
y_num_soma = [df_week_soma['likes'][0], df_week_soma['likes'][1], df_week_soma['likes'][2], df_week_soma['likes'][3],
              df_week_soma['likes'][4], df_week_soma['likes'][5], df_week_soma['likes'][6]]
y_num_comments = [df_week_soma['comentarios'][0], df_week_soma['comentarios'][1], df_week_soma['comentarios'][2], df_week_soma['comentarios'][3],
                  df_week_soma['comentarios'][4], df_week_soma['comentarios'][5], df_week_soma['comentarios'][6]]

figB1 = go.Figure()
figB1.add_trace(go.Bar(
    name='Likes', x=values, y=y_like, text=y_num_soma,
    hovertemplate="</br><b>Média de Likes:</b> %{y:.2f}" +
                   "</br><b>Total de Likes:</b> %{text}",
    textposition='none', marker_color='#E1306C'
))
figB1.add_trace(go.Bar(
    name='Comentários', x=values, y=y_comments, text=y_num_comments,
    hovertemplate="</br><b>Média de Comentários:</b> %{y:.2f}" +
                   "</br><b>Total de Comentários:</b> %{text}",
    textposition='none', marker_color='#833AB4'
))
figB1.add_trace(go.Bar(
    name='Publicações', x=values, y=y_num,
    hovertemplate="</br><b>Total de Publicações:</b> %{y}",
    textposition='none', marker_color='#405DE6'
))
figB1.update_layout(
    paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
    legend=dict(font_size=11, orientation="h", yanchor="top", y=1.20, xanchor="center", x=0.5),
    height=200, barmode='stack', margin=dict(l=1, r=1, b=1, t=1), autosize=True, hovermode="x")
figB1.update_yaxes(
    title_text="Número de Interações",title_font=dict(family='Sans-serif', size=12),
    tickfont=dict(family='Sans-serif', size=9), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')


### GRAFICO 6 - LINHA -
df_day = df.groupby('dia').agg('sum').reset_index()

figB2 = go.Figure()
figB2.add_trace(go.Scatter(
    x=df_day['dia'], y=df_day['likes'],
    name='Likes', mode='lines',  hovertemplate=None, xhoverformat="%d %b %y",
    line=dict(width=1, color='#E1306C'), stackgroup='one'))

figB2.add_trace(go.Scatter(
    x=df_day['dia'], y=df_day['comentarios'],
    name='Comentários', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
    line=dict(width=1, color='#833AB4'), stackgroup='two'))

figB2.add_trace(go.Scatter(
    x=df_day['dia'], y=df_day['conta'],
    name='Publicações', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
    line=dict(width=1, color='#405DE6'), stackgroup='three'))

figB2.update_layout(
    paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
    legend=dict(font_size=12, orientation="h", yanchor="top", y=1.20, xanchor="center", x=0.5),
    height=220, hovermode="x unified", margin=dict(l=1, r=1, b=1, t=1))
figB2.update_xaxes(
    rangeslider_visible=True)
figB2.update_yaxes(
    title_text="Número de Interações", title_font=dict(family='Sans-serif', size=12),
    tickfont=dict(family='Sans-serif', size=9), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

#############################################################################################################
#####################################################################################################3########

df_map = df.groupby(['semana', 'Turno']).agg('sum').reset_index()

seg_MN=df_map["inter"].iloc[1]; seg_TD=df_map["inter"].iloc[3]; seg_NT=df_map["inter"].iloc[2]; seg_MD=df_map["inter"].iloc[0];
ter_MN=df_map["inter"].iloc[5]; ter_TD=df_map["inter"].iloc[7]; ter_NT=df_map["inter"].iloc[6]; ter_MD=df_map["inter"].iloc[4];
qua_MN=df_map["inter"].iloc[9]; qua_TD=df_map["inter"].iloc[11]; qua_NT=df_map["inter"].iloc[10]; qua_MD=df_map["inter"].iloc[8];
qui_MN=df_map["inter"].iloc[13]; qui_TD=df_map["inter"].iloc[15]; qui_NT=df_map["inter"].iloc[14]; qui_MD=df_map["inter"].iloc[12];
sex_MN=df_map["inter"].iloc[17]; sex_TD=df_map["inter"].iloc[19]; sex_NT=df_map["inter"].iloc[18]; sex_MD=df_map["inter"].iloc[16];
sab_MN=df_map["inter"].iloc[21]; sab_TD=df_map["inter"].iloc[23]; sab_NT=df_map["inter"].iloc[22]; sab_MD=df_map["inter"].iloc[20];
dom_MN=df_map["inter"].iloc[25]; dom_TD=df_map["inter"].iloc[27]; dom_NT=df_map["inter"].iloc[26]; dom_MD=df_map["inter"].iloc[24];

matriz = [[dom_MD, seg_MD, ter_MD, qua_MD, qui_MD, sex_MD, sab_MD],
          [dom_NT, seg_NT, ter_NT, qua_NT, qui_NT, sex_NT, sab_NT],
          [dom_TD, seg_TD, ter_TD, qua_TD, qui_TD, sex_TD, sab_TD],
          [dom_MN, seg_MN, ter_MN, qua_MN, qui_MN, sex_MN, sab_MN]]

figC2 = go.Figure(data=go.Heatmap(
                   z=matriz, name="", text=matriz,
                   x=['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'],
                   y=['Madrugada', 'Noite', 'Tarde', 'Manhã'],
                   texttemplate="%{text}",
                   hovertemplate="</br><b>Dia:</b> %{x}"+
                                 "</br><b>Turno:</b> %{y}"+
                                 "</br><b>Interações:</b> %{z}",
                   colorscale='Portland'))
figC2.update_layout(autosize=True,
                   height=200, margin=dict(l=1, r=10, b=10, t=15),
                   paper_bgcolor="#F8F8FF", font={'size': 12})



seg_MN=df_map["conta"].iloc[1]; seg_TD=df_map["conta"].iloc[3]; seg_NT=df_map["conta"].iloc[2]; seg_MD=df_map["conta"].iloc[0];
ter_MN=df_map["conta"].iloc[5]; ter_TD=df_map["conta"].iloc[7]; ter_NT=df_map["conta"].iloc[6]; ter_MD=df_map["conta"].iloc[4];
qua_MN=df_map["conta"].iloc[9]; qua_TD=df_map["conta"].iloc[11]; qua_NT=df_map["conta"].iloc[10]; qua_MD=df_map["conta"].iloc[8];
qui_MN=df_map["conta"].iloc[13]; qui_TD=df_map["conta"].iloc[15]; qui_NT=df_map["conta"].iloc[14]; qui_MD=df_map["conta"].iloc[12];
sex_MN=df_map["conta"].iloc[17]; sex_TD=df_map["conta"].iloc[19]; sex_NT=df_map["conta"].iloc[18]; sex_MD=df_map["conta"].iloc[16];
sab_MN=df_map["conta"].iloc[21]; sab_TD=df_map["conta"].iloc[23]; sab_NT=df_map["conta"].iloc[22]; sab_MD=df_map["conta"].iloc[20];
dom_MN=df_map["conta"].iloc[25]; dom_TD=df_map["conta"].iloc[27]; dom_NT=df_map["conta"].iloc[26]; dom_MD=df_map["conta"].iloc[24];

matriz = [[dom_MD, seg_MD, ter_MD, qua_MD, qui_MD, sex_MD, sab_MD],
          [dom_NT, seg_NT, ter_NT, qua_NT, qui_NT, sex_NT, sab_NT],
          [dom_TD, seg_TD, ter_TD, qua_TD, qui_TD, sex_TD, sab_TD],
          [dom_MN, seg_MN, ter_MN, qua_MN, qui_MN, sex_MN, sab_MN]]

figC1 = go.Figure(data=go.Heatmap(
                   z=matriz, name="", text=matriz,
                   x=['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'],
                   y=['Madrugada', 'Noite', 'Tarde', 'Manhã'],
                   texttemplate="%{text}",
                   hovertemplate="</br><b>Dia:</b> %{x}"+
                                 "</br><b>Turno:</b> %{y}"+
                                 "</br><b>Publicações:</b> %{z}",
                   colorscale='Portland'))
figC1.update_layout(autosize=True,
                   height=200, margin=dict(l=1, r=10, b=10, t=15),
                   paper_bgcolor="#F8F8FF", font={'size': 12})


words = ' '.join(df['descricao'])

figD1, ax = plt.subplots()
wordcloud = WordCloud(
                    height=200,
                    min_font_size=8,
                    scale=2.5,
                    background_color='#F9F9FA',
                    max_words=50,
                    min_word_length=2).generate(words)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off') # to off the axis of x and



def folha_tabela(df):

    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_pagination(enabled=True)
    gd.configure_default_column(editable=False)
    gd.configure_selection(use_checkbox=True, selection_mode='multiple')
    gd.configure_side_bar()
    gridoptions = gd.build()
    df_grid = AgGrid(df, gridOptions=gridoptions, enable_enterprise_modules=True,
                     update_mode=GridUpdateMode.SELECTION_CHANGED, height=250, width='100%')
    selected_rows = df_grid["selected_rows"]
    selected_rows = pd.DataFrame(selected_rows)

    return selected_rows