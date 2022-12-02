import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import numpy as np
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import STOPWORDS
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

im1 = Image.open("image/publicacao.jpeg")
im2 = Image.open("image/like.png")
im3 = Image.open("image/comentario.png")

### GRAFICO INDICADOR - MÉTRICAS GLOBAIS, LIKES E COMENTÁRIOS
# DADOS DE ENTRADA:

@st.cache(suppress_st_warning=True)
def metricas(df):
    df_metricas = df.describe().reset_index()
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

    # CONFIGURANDO GRAFICO INDICADOR 2 -  METRICAS LIKES
    fig1 = go.Figure()
    fig1.add_trace(go.Indicator(
        mode="number",
        number_font_size=22,
        number_font_color="#FD1D1D",
        value=soma_post_like,
        title={"text": "<span style='font-size:16px;color:black'>Total:</span>"},
        domain = {'y': [0, 1], 'x': [0.2, 0.5]}))
    fig1.add_trace(go.Indicator(
        mode="number",
        number_font_size=22,
        number_font_color="#FD1D1D",
        value=media_post_like,
        title={"text": "<span style='font-size:16px;color:black'>Média:</span>"},
        domain = {'y': [0, 1], 'x': [0.5, 0.7]}))
    fig1.add_trace(go.Indicator(
        mode="number",
        number_font_size=22,
        number_font_color="#FD1D1D",
        value=max_post_like,
        title={"text": "<span style='font-size:16px;color:black'>Máximo:</span>"},
        domain = {'y': [0, 1], 'x': [0.7, 1]}))
    fig1.update_layout(
        paper_bgcolor="#F8F8FF", height=90, margin=dict(l=1, r=1, b=1, t=30),
        grid={'rows': 1, 'columns': 3})

    fig1.add_layout_image(dict(source=im2, xref="paper", yref="paper", x=0.05, y=0.75, xanchor='left', yanchor='middle',
                              sizex=1.0, sizey=1.0))

    fig2 = go.Figure()
    fig2.add_trace(go.Indicator(
        mode="number",
        number_font_size=22,
        number_font_color="#F56040",
        value=soma_post_comments,
        title={"text": "<span style='font-size:16px;color:black'>Total:</span>"},
        domain={'y': [0, 1], 'x': [0.2, 0.5]}))
    fig2.add_trace(go.Indicator(
        mode="number",
        number_font_size=22,
        number_font_color="#F56040",
        value=media_post_comments,
        title={"text": "<span style='font-size:16px;color:black'>Média:</span>"},
        domain={'y': [0, 1], 'x': [0.5, 0.7]}))
    fig2.add_trace(go.Indicator(
        mode="number",
        number_font_size=22,
        number_font_color="#F56040",
        value=max_post_comments,
        title={"text": "<span style='font-size:16px;color:black'>Máximo:</span>"},
        domain={'y': [0, 1], 'x': [0.7, 1]}))
    fig2.update_layout(
        paper_bgcolor="#F8F8FF", height=90, margin=dict(l=1, r=1, b=0, t=30),
        grid={'rows': 1, 'columns': 3})

    fig2.add_layout_image(
        dict(source=im3, xref="paper", yref="paper", x=0.01, y=0.75, xanchor='left', yanchor='middle',
             sizex=0.90, sizey=0.9))

    return fig1, fig2

# CONFIGURANDO GRAFICO INDICADOR 3 -  METRICAS COMENTÁRIOS

@st.cache(suppress_st_warning=True)
def pie3(df):

    df_type = df.groupby('tipo').agg('sum').reset_index()
    df_ima = df_type.query("tipo == 'Imagem'")
    df_col = df_type.query("tipo == 'Coleção'")
    df_vid = df_type.query("tipo == 'Vídeo'")

    try:
        IMAGEM = df_ima["UNIDADE"].iloc[0]
        IMAGEM_LIKES = df_ima["likes"].iloc[0]
        IMAGEM_COMENTARIOS = df_ima["comentarios"].iloc[0]
    except:
        IMAGEM = 0
        IMAGEM_LIKES = 0
        IMAGEM_COMENTARIOS = 0

    try:
        VIDEO = df_vid["UNIDADE"].iloc[0]
        VIDEO_LIKES = df_vid["likes"].iloc[0]
        VIDEO_COMENTARIOS = df_vid["comentarios"].iloc[0]
    except:
        VIDEO = 0
        VIDEO_LIKES = 0
        VIDEO_COMENTARIOS = 0

    try:
        COLECAO = df_col["UNIDADE"].iloc[0]
        COLECAO_LIKES = df_col["likes"].iloc[0]
        COLECAO_COMENTARIOS = df_col["comentarios"].iloc[0]
    except:
        COLECAO = 0
        COLECAO_LIKES = 0
        COLECAO_COMENTARIOS = 0

    labels = ['Imagem', "Coleção", 'Vídeo']
    colors = ['#E1306C', '#C13584', '#833AB4']
    fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]],
                          subplot_titles=['Publicações:', 'Likes:', 'Comentários:'])

    fig.add_trace(go.Pie(labels=labels, name="Publicações",
                           values=[IMAGEM, COLECAO, VIDEO],
                           textinfo='none', showlegend=True,
                           domain={'y': [0, 1], 'x': [0, 0.3]},
                           marker=dict(colors=colors, line=dict(color='#000010', width=2))))

    fig.add_trace(go.Pie(labels=labels, name="Likes",
                           values=[IMAGEM_LIKES, COLECAO_LIKES, VIDEO_LIKES],
                           textinfo='none', showlegend=True,
                           domain={'y': [0, 1], 'x': [0.35, 0.65]},
                           marker=dict(colors=colors, line=dict(color='#000010', width=2))))
    fig.add_trace(go.Pie(labels=labels, name="Comentários",
                           values=[IMAGEM_COMENTARIOS, COLECAO_COMENTARIOS, VIDEO_COMENTARIOS],
                           textinfo='none', showlegend=True,
                           domain={'y': [0, 1], 'x': [0.7, 1]},
                           marker=dict(colors=colors, line=dict(color='#000010', width=2))))

    fig.update_traces(hole=.4, hoverinfo="label+name+percent+value",
                        hovertemplate="</br><b>Publicação:</b> %{label} " +
                                      "</br><b>Quantidade:</b>  %{value}" +
                                      "</br><b>Proporção:</b>  %{percent}")
    fig.update_layout(autosize=True,
                       height=200, margin=dict(l=10, r=10, b=20, t=40),
                       legend=dict(font_size=14, orientation="h", yanchor="top",
                                   y=-0.05, xanchor="center", x=0.5),
                       paper_bgcolor="#F8F8FF", font={'size': 20})


    return fig

##############################################################################################################
###############################################################################################################

@st.cache(suppress_st_warning=True)
def bar(df):

    df_ws = df.groupby('semana').agg('sum').reset_index()

    df_ws.loc[df_ws['semana'] == 'Domingo', 'order'] = 1
    df_ws.loc[df_ws['semana'] == 'Segunda', 'order'] = 2
    df_ws.loc[df_ws['semana'] == 'Terça', 'order'] = 3
    df_ws.loc[df_ws['semana'] == 'Quarta', 'order'] = 4
    df_ws.loc[df_ws['semana'] == 'Quinta', 'order'] = 5
    df_ws.loc[df_ws['semana'] == 'Sexta', 'order'] = 6
    df_ws.loc[df_ws['semana'] == 'Sábado', 'order'] = 7

    df_ws = df_ws.sort_values(by=['order'], ascending=True)

    y_num = df_ws['UNIDADE']
    y_num_soma = df_ws['likes']
    y_num_comments = df_ws['comentarios']

    values = df_ws.semana.unique()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Likes', x=values, y=y_num_soma,
        hovertemplate="</br><b>Total de Likes:</b> %{y:,.0f}",
        textposition='none', marker_color='#E1306C'
    ))
    fig.add_trace(go.Bar(
        name='Comentários', x=values, y=y_num_comments,
        hovertemplate="</br><b>Total de Comentários:</b> %{y:,.0f}",
        textposition='none', marker_color='#833AB4'
    ))
    fig.add_trace(go.Bar(
        name='Publicações', x=values, y=y_num,
        hovertemplate="</br><b>Total de Publicações:</b> %{y:,.0f}",
        textposition='none', marker_color='#405DE6'
    ))
    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=11, orientation="h", yanchor="top", y=1.20, xanchor="center", x=0.5),
        height=200, barmode='stack', margin=dict(l=1, r=1, b=1, t=1), autosize=True, hovermode="x")
    fig.update_yaxes(
        title_text="Número de Interações",title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=9), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    return fig


@st.cache(suppress_st_warning=True)
def bar_hora(df):
    df_week = df.groupby('hora').agg('mean').reset_index()
    df_week_soma = df.groupby('hora').agg('sum').reset_index()

    values = df_week.hora.unique()
    y_like = df_week['likes']
    y_comments = df_week['comentarios']

    y_num = df_week_soma['UNIDADE']
    y_num_soma = df_week_soma['likes']
    y_num_comments = df_week_soma['comentarios']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Likes', x=values, y=y_num_soma,
        hovertemplate="</br><b>Total de Likes:</b> %{y:,.0f}",
        textposition='none', marker_color='#E1306C'
    ))
    fig.add_trace(go.Bar(
        name='Comentários', x=values, y=y_num_comments,
        hovertemplate="</br><b>Total de Comentários:</b> %{y:,.0f}",
        textposition='none', marker_color='#833AB4'
    ))
    fig.add_trace(go.Bar(
        name='Publicações', x=values, y=y_num,
        hovertemplate="</br><b>Total de Publicações:</b> %{y:,.0f}",
        textposition='none', marker_color='#405DE6'
    ))
    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=11, orientation="h", yanchor="top", y=1.20, xanchor="center", x=0.5),
        height=200, barmode='stack', margin=dict(l=1, r=1, b=1, t=1), autosize=True, hovermode="x", )
    fig.update_yaxes(
        title_text="Número de Interações",title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=9), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    fig.update_xaxes(
        tickfont=dict(family='Sans-serif', size=9), nticks=20, showgrid=False)

    return fig

@st.cache(suppress_st_warning=True)
def bar_nomes(df):
    df_week_soma = df.groupby('Nome').agg('sum').reset_index()

    values = df_week_soma.Nome.unique()

    y_num = df_week_soma['UNIDADE']
    y_num_soma = df_week_soma['likes']
    y_num_comments = df_week_soma['comentarios']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Likes', x=values, y=y_num_soma,
        hovertemplate="</br><b>Total de Likes:</b> %{y:,.0f}",
        textposition='none', marker_color='#E1306C'
    ))
    fig.add_trace(go.Bar(
        name='Comentários', x=values, y=y_num_comments,
        hovertemplate="</br><b>Total de Comentários:</b> %{y:,.0f}",
        textposition='none', marker_color='#833AB4'
    ))
    fig.add_trace(go.Bar(
        name='Publicações', x=values, y=y_num,
        hovertemplate="</br><b>Total de Publicações:</b> %{y:,.0f}",
        textposition='none', marker_color='#405DE6'
    ))
    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=11, orientation="h", yanchor="top", y=1.20, xanchor="center", x=0.5),
        height=220, barmode='stack', margin=dict(l=1, r=1, b=1, t=1), autosize=True, hovermode="x", )
    fig.update_yaxes(
        title_text="Número de Interações",title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=9), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    fig.update_xaxes(
        tickfont=dict(family='Sans-serif', size=9), nticks=20, showgrid=False)

    return fig

@st.cache(suppress_st_warning=True)
def linha(df):

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
        x=df_day['dia'], y=df_day['UNIDADE'],
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
    return figB2




def linha_nome(df):

    df['Metropoles'] = np.where(df['Nome'] == 'Metropoles', 1, 0)
    df['Folha de S.Paulo'] = np.where(df['Nome'] == 'Folha de S.Paulo', 1, 0)
    df['UOL'] = np.where(df['Nome'] == 'UOL', 1, 0)
    df['Estadão'] = np.where(df['Nome'] == 'Estadão', 1, 0)
    df['O Globo'] = np.where(df['Nome'] == 'O Globo', 1, 0)
    df['CNN Brasil'] = np.where(df['Nome'] == 'CNN Brasil', 1, 0)
    df['Jovem Pan'] = np.where(df['Nome'] == 'Jovem Pan', 1, 0)
    df['Portal R7'] = np.where(df['Nome'] == 'Portal R7', 1, 0)
    df['Portal G1'] = np.where(df['Nome'] == 'Portal G1', 1, 0)
    df['BBC News'] = np.where(df['Nome'] == 'BBC News', 1, 0)

    #df_day = df.groupby('dia').agg('sum').reset_index()

    df_day = df.groupby(['dia', 'Nome']).agg('sum').reset_index()
    df_met = df_day.query("Nome == 'Metropoles'")
    df_fol = df_day.query("Nome == 'Folha de S.Paulo'")
    df_uol = df_day.query("Nome == 'UOL'")
    df_est = df_day.query("Nome == 'Estadão'")
    df_glo = df_day.query("Nome == 'O Globo'")
    df_cnn = df_day.query("Nome == 'CNN Brasil'")
    df_jpn = df_day.query("Nome == 'Jovem Pan'")
    df_pr7 = df_day.query("Nome == 'Portal R7'")
    df_pg1 = df_day.query("Nome == 'Portal G1'")
    df_bbc = df_day.query("Nome == 'BBC News'")

    figB2 = go.Figure()
    figB2.add_trace(go.Scatter(
        x=df_met['dia'], y=df_met['inter'],
        name='Metropoles', mode='lines',  hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#C41A1B'), stackgroup='one'))

    figB2.add_trace(go.Scatter(
        x=df_fol['dia'], y=df_fol['inter'],
        name='Folha de S.Paulo', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#008B8B'), stackgroup='two'))

    figB2.add_trace(go.Scatter(
        x=df_uol['dia'], y=df_uol['inter'],
        name='UOL', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#FECB17'), stackgroup='three'))
    figB2.add_trace(go.Scatter(
        x=df_est['dia'], y=df_est['inter'],
        name='Estadão', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#405DE6'), stackgroup='four'))
    figB2.add_trace(go.Scatter(
        x=df_glo['dia'], y=df_glo['inter'],
        name='O Globo', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#004787'), stackgroup='five'))
    figB2.add_trace(go.Scatter(
        x=df_cnn['dia'], y=df_cnn['inter'],
        name='CNN Brasil', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#ff4500'), stackgroup='six'))

    figB2.add_trace(go.Scatter(
        x=df_jpn['dia'], y=df_jpn['inter'],
        name='Jovem Pan', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#2F4F4F'), stackgroup='seven'))
    figB2.add_trace(go.Scatter(
        x=df_pr7['dia'], y=df_pr7['inter'],
        name='Portal R7', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#2bb003'), stackgroup='eight'))
    figB2.add_trace(go.Scatter(
        x=df_pg1['dia'], y=df_pg1['inter'],
        name='Portal G1', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#ff0000'), stackgroup='nine'))
    figB2.add_trace(go.Scatter(
        x=df_bbc['dia'], y=df_bbc['inter'],
        name='BBC News', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#A52A2A'), stackgroup='ten'))


    figB2.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=12, orientation="h", yanchor="top", y=1.40, xanchor="left", x=0.06),
        height=220, hovermode="x unified", margin=dict(l=1, r=1, b=1, t=1))
    figB2.update_xaxes(
        rangeslider_visible=True)
    figB2.update_yaxes(
        title_text="Número de Interações", title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=9), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')
    return figB2


def linha_nome2(df):

    df['Metropoles'] = np.where(df['Nome'] == 'Metropoles', 1, 0)
    df['Folha de S.Paulo'] = np.where(df['Nome'] == 'Folha de S.Paulo', 1, 0)
    df['UOL'] = np.where(df['Nome'] == 'UOL', 1, 0)
    df['Estadão'] = np.where(df['Nome'] == 'Estadão', 1, 0)
    df['O Globo'] = np.where(df['Nome'] == 'O Globo', 1, 0)
    df['CNN Brasil'] = np.where(df['Nome'] == 'CNN Brasil', 1, 0)
    df['Jovem Pan'] = np.where(df['Nome'] == 'Jovem Pan', 1, 0)
    df['Portal R7'] = np.where(df['Nome'] == 'Portal R7', 1, 0)
    df['Portal G1'] = np.where(df['Nome'] == 'Portal G1', 1, 0)
    df['BBC News'] = np.where(df['Nome'] == 'BBC News', 1, 0)

    df_day = df.groupby('dia').agg('sum').reset_index()


    figB2 = go.Figure()
    figB2.add_trace(go.Scatter(
        x=df_day['dia'], y=df_day['Metropoles'],
        name='Metropoles', mode='lines',  hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#C41A1B'), stackgroup='one'))

    figB2.add_trace(go.Scatter(
        x=df_day['dia'], y=df_day['Folha de S.Paulo'],
        name='Folha de S.Paulo', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#008B8B'), stackgroup='two'))

    figB2.add_trace(go.Scatter(
        x=df_day['dia'], y=df_day['UOL'],
        name='UOL', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#FECB17'), stackgroup='three'))
    figB2.add_trace(go.Scatter(
        x=df_day['dia'], y=df_day['Estadão'],
        name='Estadão', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#405DE6'), stackgroup='four'))
    figB2.add_trace(go.Scatter(
        x=df_day['dia'], y=df_day['O Globo'],
        name='O Globo', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#004787'), stackgroup='five'))
    figB2.add_trace(go.Scatter(
        x=df_day['dia'], y=df_day['CNN Brasil'],
        name='CNN Brasil', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#ff4500'), stackgroup='six'))

    figB2.add_trace(go.Scatter(
        x=df_day['dia'], y=df_day['Jovem Pan'],
        name='Jovem Pan', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#2F4F4F'), stackgroup='seven'))
    figB2.add_trace(go.Scatter(
        x=df_day['dia'], y=df_day['Portal R7'],
        name='Portal R7', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#2bb003'), stackgroup='eight'))
    figB2.add_trace(go.Scatter(
        x=df_day['dia'], y=df_day['Portal G1'],
        name='Portal G1', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#ff0000'), stackgroup='nine'))
    figB2.add_trace(go.Scatter(
        x=df_day['dia'], y=df_day['BBC News'],
        name='BBC News', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=2, color='#A52A2A'), stackgroup='ten'))


    figB2.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=12, orientation="h", yanchor="top", y=1.40, xanchor="left", x=0.06),
        height=220, hovermode="x unified", margin=dict(l=1, r=1, b=1, t=1))
    figB2.update_xaxes(
        rangeslider_visible=True)
    figB2.update_yaxes(
        title_text="Número de Interações", title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=9), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')
    return figB2


#############################################################################################################
#####################################################################################################3########
@st.cache(suppress_st_warning=True)
def map(df):

    df_map = df.groupby(['semana', 'Turno']).agg('sum').reset_index()

    dom_MN=df_map["inter"].iloc[1]; dom_TD=df_map["inter"].iloc[3]; dom_NT=df_map["inter"].iloc[2]; dom_MD=df_map["inter"].iloc[0];
    qua_MN=df_map["inter"].iloc[5]; qua_TD=df_map["inter"].iloc[7]; qua_NT=df_map["inter"].iloc[6]; qua_MD=df_map["inter"].iloc[4];
    qui_MN=df_map["inter"].iloc[9]; qui_TD=df_map["inter"].iloc[11]; qui_NT=df_map["inter"].iloc[10]; qui_MD=df_map["inter"].iloc[8];
    seg_MN=df_map["inter"].iloc[13]; seg_TD=df_map["inter"].iloc[15]; seg_NT=df_map["inter"].iloc[14]; seg_MD=df_map["inter"].iloc[12];
    sex_MN=df_map["inter"].iloc[17]; sex_TD=df_map["inter"].iloc[19]; sex_NT=df_map["inter"].iloc[18]; sex_MD=df_map["inter"].iloc[16];
    sab_MN=df_map["inter"].iloc[21]; sab_TD=df_map["inter"].iloc[23]; sab_NT=df_map["inter"].iloc[22]; sab_MD=df_map["inter"].iloc[20];
    ter_MN=df_map["inter"].iloc[25]; ter_TD=df_map["inter"].iloc[27]; ter_NT=df_map["inter"].iloc[26]; ter_MD=df_map["inter"].iloc[24];





    matriz = [[dom_MD, seg_MD, ter_MD, qua_MD, qui_MD, sex_MD, sab_MD],
              [dom_NT, seg_NT, ter_NT, qua_NT, qui_NT, sex_NT, sab_NT],
              [dom_TD, seg_TD, ter_TD, qua_TD, qui_TD, sex_TD, sab_TD],
              [dom_MN, seg_MN, ter_MN, qua_MN, qui_MN, sex_MN, sab_MN]]

    figC2 = go.Figure(data=go.Heatmap(
                       z=matriz, name="", text=matriz,
                       x=['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'],
                       y=['Madrugada', 'Noite', 'Tarde', 'Manhã'],
                       texttemplate="%{text:,.0f}",
                       hovertemplate="</br><b>Dia:</b> %{x}"+
                                     "</br><b>Turno:</b> %{y}"+
                                     "</br><b>Interações:</b> %{z:,.0f}",
                       colorscale='Portland'))
    figC2.update_layout(autosize=True,
                       height=200, margin=dict(l=1, r=10, b=10, t=15),
                       paper_bgcolor="#F8F8FF", font={'size': 12})

    dom_MN = df_map["UNIDADE"].iloc[1]; dom_TD = df_map["UNIDADE"].iloc[3]; dom_NT = df_map["UNIDADE"].iloc[2]; dom_MD = df_map["UNIDADE"].iloc[0];
    qua_MN = df_map["UNIDADE"].iloc[5]; qua_TD = df_map["UNIDADE"].iloc[7]; qua_NT = df_map["UNIDADE"].iloc[6]; qua_MD = df_map["UNIDADE"].iloc[4];
    qui_MN = df_map["UNIDADE"].iloc[9]; qui_TD = df_map["UNIDADE"].iloc[11]; qui_NT = df_map["UNIDADE"].iloc[10]; qui_MD = df_map["UNIDADE"].iloc[8];
    seg_MN = df_map["UNIDADE"].iloc[13]; seg_TD = df_map["UNIDADE"].iloc[15]; seg_NT = df_map["UNIDADE"].iloc[14]; seg_MD = df_map["UNIDADE"].iloc[12];
    sex_MN = df_map["UNIDADE"].iloc[17]; sex_TD = df_map["UNIDADE"].iloc[19]; sex_NT = df_map["UNIDADE"].iloc[18]; sex_MD = df_map["UNIDADE"].iloc[16];
    sab_MN = df_map["UNIDADE"].iloc[21]; sab_TD = df_map["UNIDADE"].iloc[23]; sab_NT = df_map["UNIDADE"].iloc[22]; sab_MD = df_map["UNIDADE"].iloc[20];
    ter_MN = df_map["UNIDADE"].iloc[25]; ter_TD = df_map["UNIDADE"].iloc[27]; ter_NT = df_map["UNIDADE"].iloc[26]; ter_MD = df_map["UNIDADE"].iloc[24];

    matriz = [[dom_MD, seg_MD, ter_MD, qua_MD, qui_MD, sex_MD, sab_MD],
              [dom_NT, seg_NT, ter_NT, qua_NT, qui_NT, sex_NT, sab_NT],
              [dom_TD, seg_TD, ter_TD, qua_TD, qui_TD, sex_TD, sab_TD],
              [dom_MN, seg_MN, ter_MN, qua_MN, qui_MN, sex_MN, sab_MN]]

    figC1 = go.Figure(data=go.Heatmap(
                       z=matriz, name="", text=matriz,
                       x=['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'],
                       y=['Madrugada', 'Noite', 'Tarde', 'Manhã'],
                       texttemplate="%{text:,.0f}",
                       hovertemplate="</br><b>Dia:</b> %{x}"+
                                     "</br><b>Turno:</b> %{y}"+
                                     "</br><b>Publicações:</b> %{z:,.0f}",
                       colorscale='Portland'))
    figC1.update_layout(autosize=True,
                       height=200, margin=dict(l=1, r=10, b=10, t=15),
                       paper_bgcolor="#F8F8FF", font={'size': 12})

    return figC1, figC2


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

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(enabled=True)
    gb.configure_column("Nome", headerCheckboxSelection=True)
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True,
                                    aggFunc="sum", editable=True)
    gb.configure_selection(use_checkbox=True, selection_mode='multiple')
    gb.configure_side_bar()
    gridoptions = gb.build()
    df_grid = AgGrid(df, gridOptions=gridoptions, enable_enterprise_modules=True,
                     update_mode=GridUpdateMode.SELECTION_CHANGED, height=350, width='100%')
    selected_rows = df_grid["selected_rows"]
    selected_rows = pd.DataFrame(selected_rows)

    return selected_rows


def simple_aggrid(df):

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(enabled=True)
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True,
                                    aggFunc="sum", editable=True)
    gb.configure_side_bar()
    gridoptions = gb.build()
    df_grid = AgGrid(df, gridOptions=gridoptions, enable_enterprise_modules=True,
                     height=300, width='100%')

    return df_grid

def plot_bar(formato, selected_rows, optionx, optiony):
    fig = go.Figure()
    if formato == "Total":
        df_sum = selected_rows.groupby([optionx])[optiony].agg('sum').reset_index().sort_values(optionx, ascending=True)
        df_quant = selected_rows[optionx].value_counts().reset_index().sort_values(by="index", ascending=True)
        x1 = df_sum[optionx]
        y1 = df_sum[optiony]
        quant = df_quant[optionx]

        fig.add_trace(go.Bar(
            x=x1, y=y1, text=quant,
            hovertemplate="</br><b>Eixo X:</b> %{x}" +
                          "</br><b>Eixo Y:</b> %{y:,.0f}" +
                          "</br><b>Publicações:</b> %{text}",
            textposition='none', marker_color=('#C13584')))

    elif formato == "Média":

        df_mean = selected_rows.groupby([optionx])[optiony].agg('mean').reset_index().sort_values(optionx,
                                                                                                  ascending=True)
        df_quant = selected_rows[optionx].value_counts().reset_index().sort_values(by="index", ascending=True)
        x1 = df_mean[optionx]
        y1 = df_mean[optiony]
        quant = df_quant[optionx]

        fig.add_trace(go.Bar(
            x=x1, y=y1, text=quant,
            hovertemplate="</br><b>Eixo X:</b> %{x}" +
                          "</br><b>Eixo Y:</b> %{y:,.0f}" +
                          "</br><b>Publicações:</b> %{text}",
            textposition='none', marker_color=('#F56040')))

    elif formato == "Por Publicação":
        selected_rows = selected_rows.sort_values(optionx, ascending=True)
        x = selected_rows[optionx]
        y = selected_rows[optiony]
        text = selected_rows["link"]

        fig.add_trace(go.Bar(
            x=x, y=y, text=text,
            hovertemplate="</br><b>Eixo X:</b> %{x}" +
                          "</br><b>Eixo Y:</b> %{y:,.0f}" +
                          "</br><b>Linkmap:</b> %{text}",
            textposition='none', marker_color=('#4B0082')))

    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=400, margin=dict(l=20, r=20, b=20, t=20),
        legend=dict(font_size=16, orientation="h", yanchor="top", y=1.1, xanchor="center", x=0.5))
    fig.update_xaxes(
        title_text="Eixo X: "+optionx, title_font=dict(family='Sans-serif', size=20),
        tickfont=dict(family='Sans-serif', size=12), nticks=15, showgrid=False)
    fig.update_yaxes(
        title_text="Eixo Y: "+optiony, title_font=dict(family='Sans-serif', size=22),
        tickfont=dict(family='Sans-serif', size=14), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    return fig



def plot_line(selected_rows, optionx, optiony, formato):


    fig = go.Figure()
    if formato == "Total":
        df_temp = selected_rows.groupby([optionx]).agg('sum').reset_index()

        fig.add_trace(go.Scatter(
            x=df_temp[optionx], y=df_temp[optiony],
            mode='lines', stackgroup='one', hovertemplate=None, line=dict(width=1, color='#C13584')))

    elif formato == "Média":
        df_temp = selected_rows.groupby([optionx]).agg('mean').reset_index()

        fig.add_trace(go.Scatter(
            x=df_temp[optionx], y=df_temp[optiony],
            mode='lines', stackgroup='one', hovertemplate=None, line=dict(width=1, color='#F56040')))

    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=400, hovermode="x unified", margin=dict(l=10, r=10, b=1, t=10))
    fig.update_xaxes(
        title_text="Eixo X: "+optionx, title_font=dict(family='Sans-serif', size=18),
        tickfont=dict(family='Sans-serif', size=12),  showgrid=False, rangeslider_visible=True)
    fig.update_yaxes(
        title_text="Eixo Y: "+optiony, title_font=dict(family='Sans-serif', size=20),
        tickfont=dict(family='Sans-serif', size=14), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    return fig


def plot_hotmap(df, formato, formato_map):
    if formato_map == "Total":
        df_map = df.groupby(['semana', 'Turno']).agg('sum').reset_index()

    elif formato_map == "Média":
        df_map = df.groupby(['semana', 'Turno']).agg('mean').reset_index()

    dom_MN = df_map[formato].iloc[1]; dom_TD = df_map[formato].iloc[3]; dom_NT = df_map[formato].iloc[2]; dom_MD = df_map[formato].iloc[0];
    qua_MN = df_map[formato].iloc[5]; qua_TD = df_map[formato].iloc[7]; qua_NT = df_map[formato].iloc[6]; qua_MD = df_map[formato].iloc[4];
    qui_MN = df_map[formato].iloc[9]; qui_TD = df_map[formato].iloc[11]; qui_NT = df_map[formato].iloc[10]; qui_MD = df_map[formato].iloc[8];
    seg_MN = df_map[formato].iloc[13]; seg_TD = df_map[formato].iloc[15]; seg_NT = df_map[formato].iloc[14]; seg_MD = df_map[formato].iloc[12];
    sex_MN = df_map[formato].iloc[17]; sex_TD = df_map[formato].iloc[19]; sex_NT = df_map[formato].iloc[18]; sex_MD = df_map[formato].iloc[16];
    sab_MN = df_map[formato].iloc[21]; sab_TD = df_map[formato].iloc[23]; sab_NT = df_map[formato].iloc[22]; sab_MD = df_map[formato].iloc[20];
    ter_MN = df_map[formato].iloc[25]; ter_TD = df_map[formato].iloc[27]; ter_NT = df_map[formato].iloc[26]; ter_MD = df_map[formato].iloc[24];

    matriz = [[dom_MD, seg_MD, ter_MD, qua_MD, qui_MD, sex_MD, sab_MD],
              [dom_NT, seg_NT, ter_NT, qua_NT, qui_NT, sex_NT, sab_NT],
              [dom_TD, seg_TD, ter_TD, qua_TD, qui_TD, sex_TD, sab_TD],
              [dom_MN, seg_MN, ter_MN, qua_MN, qui_MN, sex_MN, sab_MN]]

    fig = go.Figure(data=go.Heatmap(
        z=matriz, name="", text=matriz,
        x=['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'],
        y=['Madrugada', 'Noite', 'Tarde', 'Manhã'],
        texttemplate="%{text:,.0f}",
        hovertemplate="</br><b>Dia:</b> %{x}" +
                      "</br><b>Turno:</b> %{y}" +
                      "</br><b>Interações:</b> %{z:,.0f}",
        colorscale='Portland'))
    fig.update_layout(height=400, margin=dict(l=5, r=5, b=5, t=5),
                      paper_bgcolor="#F8F8FF", font={'size': 16})

    return fig


def plot_wordcoud(df):
    words = ' '.join(df['descricao'])
    stop_words = STOPWORDS.update(["da", "do", "a", "e", "o", "em", "para", "um",
                                   "que", "por", "como", "uma", "de", "onde", "são",
                                   "sim", "não", "mas", "mais", "então", "das", "dos", "nas", "nos",
                                   "bio", "link", "isso", "tem", "até"])

    fig, ax = plt.subplots()
    wordcloud = WordCloud(
        height=150,
        min_font_size=8,
        scale=2.5,
        background_color='#F8F8FF',
        max_words=100,
        stopwords=stop_words,
        min_word_length=3).generate(words)
    plt.imshow(wordcloud)
    plt.axis('off')  # to off the axis of x and

    return fig