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

im1 = Image.open("image/publicacao.jpeg")
im2 = Image.open("image/like.png")
im3 = Image.open("image/comentario.png")

### GRAFICO INDICADOR - MÉTRICAS GLOBAIS, LIKES E COMENTÁRIOS
# DADOS DE ENTRADA:

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

def pie3(df):

    df_type = df.groupby('tipo').agg('sum')
    IMAGEM = df_type["UNIDADE"].iloc[1]
    VIDEO = df_type["UNIDADE"].iloc[2]
    COLECAO = df_type["UNIDADE"].iloc[0]

    IMAGEM_LIKES = df_type["likes"].iloc[1]
    VIDEO_LIKES = df_type["likes"].iloc[2]
    COLECAO_LIKES = df_type["likes"].iloc[0]

    IMAGEM_COMENTARIOS = df_type["comentarios"].iloc[1]
    VIDEO_COMENTARIOS = df_type["comentarios"].iloc[2]
    COLECAO_COMENTARIOS = df_type["comentarios"].iloc[0]

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

def bar(df):
    df_week = df.groupby('semana').agg('mean')
    df_week_soma = df.groupby('semana').agg('sum')

    values = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
    y_like = [df_week['likes'][0], df_week['likes'][3], df_week['likes'][6], df_week['likes'][1],
              df_week['likes'][2], df_week['likes'][4], df_week['likes'][5]]
    y_comments = [df_week['comentarios'][0], df_week['comentarios'][3], df_week['comentarios'][6], df_week['comentarios'][1],
                  df_week['comentarios'][2], df_week['comentarios'][4], df_week['comentarios'][5]]
    y_num = [df_week_soma['UNIDADE'][0], df_week_soma['UNIDADE'][3], df_week_soma['UNIDADE'][6], df_week_soma['UNIDADE'][1],
             df_week_soma['UNIDADE'][2], df_week_soma['UNIDADE'][4], df_week_soma['UNIDADE'][5]]
    y_num_soma = [df_week_soma['likes'][0], df_week_soma['likes'][3], df_week_soma['likes'][6], df_week_soma['likes'][1],
                  df_week_soma['likes'][2], df_week_soma['likes'][4], df_week_soma['likes'][5]]
    y_num_comments = [df_week_soma['comentarios'][0], df_week_soma['comentarios'][3], df_week_soma['comentarios'][6], df_week_soma['comentarios'][1],
                      df_week_soma['comentarios'][2], df_week_soma['comentarios'][4], df_week_soma['comentarios'][5]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Likes', x=values, y=y_num_soma ,
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


#############################################################################################################
#####################################################################################################3########

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
    if formato == "Total de Atividades":
        df_sum = selected_rows.groupby([optionx])[optiony].agg('sum').reset_index().sort_values(optionx,
                                                                                                  ascending=True)
        df_quant = selected_rows[optionx].value_counts().reset_index().sort_values(by="index", ascending=True)
        x1 = df_sum[optionx]
        y1 = df_sum[optiony]
        quant = df_quant[optionx]

        fig.add_trace(go.Bar(
            x=x1, y=y1, text=quant,
            hovertemplate="</br><b>Eixo X:</b> %{x}" +
                          "</br><b>Eixo Y:</b> %{y:,.0f}" +
                          "</br><b>Publicações:</b> %{text}",
            textposition='none', marker_color=('#E1306C')))

    elif formato == "Média de Atividades":

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
            textposition='none', marker_color=('#E1306C')))

    elif formato == "Atividades por Publicação":
        selected_rows = selected_rows.sort_values(optionx, ascending=True)
        x = selected_rows[optionx]
        y = selected_rows[optiony]
        text = selected_rows["shortcode"]

        fig.add_trace(go.Bar(
            x=x, y=y, text=text,
            hovertemplate="</br><b>Eixo X:</b> %{x}" +
                          "</br><b>Eixo Y:</b> %{y:,.0f}" +
                          "</br><b>Shortcode:</b> %{text}",
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



def plot_line(selected_rows, optionx, optiony):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=selected_rows[optionx], y=selected_rows[optiony],
        mode='lines', stackgroup='one', hovertemplate=None, line=dict(width=1, color='#4169E1')))
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


def plot_hotmap(df, formato):
    df_map = df.groupby(['semana', 'Turno']).agg('sum').reset_index()

    seg_MN = df_map[formato].iloc[1]; seg_TD = df_map[formato].iloc[3]; seg_NT = df_map[formato].iloc[2]; seg_MD = df_map[formato].iloc[0];
    ter_MN = df_map[formato].iloc[5]; ter_TD = df_map[formato].iloc[7]; ter_NT = df_map[formato].iloc[6]; ter_MD = df_map[formato].iloc[4];
    qua_MN = df_map[formato].iloc[9]; qua_TD = df_map[formato].iloc[11]; qua_NT = df_map[formato].iloc[10]; qua_MD = df_map[formato].iloc[8];
    qui_MN = df_map[formato].iloc[13]; qui_TD = df_map[formato].iloc[15]; qui_NT = df_map[formato].iloc[14]; qui_MD = df_map[formato].iloc[12];
    sex_MN = df_map[formato].iloc[17]; sex_TD = df_map[formato].iloc[19]; sex_NT = df_map[formato].iloc[18]; sex_MD = df_map[formato].iloc[16];
    sab_MN = df_map[formato].iloc[21];  sab_TD = df_map[formato].iloc[23]; sab_NT = df_map[formato].iloc[22]; sab_MD = df_map[formato].iloc[20];
    dom_MN = df_map[formato].iloc[25]; dom_TD = df_map[formato].iloc[27]; dom_NT = df_map[formato].iloc[26]; dom_MD = df_map[formato].iloc[24];

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