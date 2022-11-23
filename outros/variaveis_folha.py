from PIL import Image

# CAMINHO PARA OS DADOS ----------------------------------------------------------------

path_posts = "df150-folhadespaulo-tratado.csv"
#path_comentarios = "instagram_allcomments.csv"

path_globo = "df150-globo-tratado.csv"

path_estadao = "df150-estadao-tratado.csv"

path_uol = "df150-uol-tratado.csv"

path_cnn = "df150-cnn-tratado.csv"

path_choquei = "df150-choquei-tratado.csv"
path_todos = "todos-tratado.csv"

# - TOPO E RODAPÉ ------------------------------------------------------------------------
html_title="""
<h1 style="font-size:200%; color:#5B51D8; font-family:sans-serif;
            text-align:center; ">Instagram Monitor Interativo</h1>
"""
html_rodape="""
<hr style= "display: block;
  margin-top: 0.5em;
  margin-bottom: 0.5em;
  margin-left: auto;
  margin-right: auto;
  border-style: inset;
  border-width: 1.5px;">
  <p style="color:Gainsboro; text-align: center;">Última atualização: 27/10/2022</p>
"""



# - PARTE 1 ------------------------------------------------------------------
## 1.1 - Número de Doses & Vacinas Aplicadas:
html_subheader_11="""
<div class="card">
  <div class="card-body" style="border-radius: 50px 50px 50px 50px; background: #5B51D8; 
                                border:solid; border-color: black; border-width: 2px 2px 2px 2px;
                                padding-top: 1px; padding-right: 25px; padding-bottom: 1px; padding-left: 25px; 
                                width: 100%; height: 60px;">
    <h3 class="card-title" style="background-color:#5B51D8; color:#F5F5F5; 
                                  font-family:sans-serif; text-align: center; 
                                  padding-top: 20px; padding-right: 1px; padding-bottom: 0px; padding-left: 1px;
                                  font-size:150%;" 
                                  >Monitoramento das Publicações</h3>
  </div>
"""

html_header_10="""
<div class="card">
  <div class="card-body">
    <h2 class="card-title" style="color:#5B51D8; font-family:sans-serif; 
                                  text-align: center; padding: 10px 0; font-size:220%;"
                                  >Monitoramento das Publicações</h2>
  </div>
</div>
"""

html_card_header_AA1="""
<div class="card">
  <div class="card-body" style="border-radius: 15px 15px 0px 0px; background: #5B51D8;  
                                border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                                padding-top: 1px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px; 
                                width: 100%; height: 40px;">
    <h5 class="card-title" style="background-color:#5B51D8; color:#F5F5F5; font-family:sans-serif;
                                  padding-top: 7px; padding-right: 1px; padding-bottom: 1px; padding-left: 1px; 
                                  text-align: center;font-size: 120%;" 
                                  >Indicadores Chaves</h5>
  </div>
</div>
"""

html_card_header_ABB="""
<div class="card">
  <div class="card-body" style="border-radius: 15px 15px 0px 0px; background: #5B51D8;  
                                border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                                padding-top: 1px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px; 
                                width: 100%; height: 40px;">
    <h5 class="card-title" style="background-color:#5B51D8; color:#F5F5F5; font-family:sans-serif;
                                  padding-top: 7px; padding-right: 15px; padding-bottom: 1px; padding-left: 15px; 
                                  text-align: center;font-size: 110%;" 
                                  >Indicadores por Tipo de Publicação</h5>
  </div>
</div>
"""

html_card_header_AB="""
<div class="card">
  <div class="card-body" style="border-radius: 15px 15px 0px 0px; background: #4169E1;  
                                border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                                padding-top: 1px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px; 
                                width: 100%; height: 40px;">
    <h5 class="card-title" style="background-color:#4169E1; color:#F5F5F5; font-family:sans-serif;
                                  padding-top: 7px; padding-right: 15px; padding-bottom: 1px; padding-left: 15px; 
                                  text-align: center;font-size: 120%;" 
                                  >Interações por Tipo de Publicação</h5>
  </div>
</div>
"""


html_card_header_BA="""
<div class="card">
  <div class="card-body" style="border-radius: 15px 15px 0px 0px; background: #4169E1;  
                                border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                                padding-top: 1px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px; 
                                width: 100%; height: 40px;">
    <h5 class="card-title" style="background-color:#4169E1; color:#F5F5F5; font-family:sans-serif;
                                  padding-top: 7px; padding-right: 15px; padding-bottom: 1px; padding-left: 15px; 
                                  text-align: center;font-size: 120%;" 
                                  >Média de Interações por Dia da Semana</h5>
  </div>
</div>
"""

html_card_header_BB="""
<div class="card">
  <div class="card-body" style="border-radius: 15px 15px 0px 0px; background: #4169E1;  
                                border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                                padding-top: 1px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px; 
                                width: 100%; height: 40px;">
    <h5 class="card-title" style="background-color:#4169E1; color:#F5F5F5; font-family:sans-serif;
                                  padding-top: 7px; padding-right: 15px; padding-bottom: 1px; padding-left: 15px; 
                                  text-align: center;font-size: 120%;" 
                                  >Variação de Interações por Dia</h5>
  </div>
</div>
"""


html_card_header_CA="""
<div class="card">
  <div class="card-body" style="border-radius: 15px 15px 0px 0px; background: #4169E1;  
                                border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                                padding-top: 1px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px; 
                                width: 100%; height: 40px;">
    <h5 class="card-title" style="background-color:#4169E1; color:#F5F5F5; font-family:sans-serif;
                                  padding-top: 7px; padding-right: 15px; padding-bottom: 1px; padding-left: 15px; 
                                  text-align: center;font-size: 120%;" 
                                  >Tabela com Dados das Publicações</h5>
  </div>
</div>
"""
html_card_header_1D2="""
<div class="card">
  <div class="card-body" style="border-radius: 15px 15px 0px 0px; background: #4169E1;  
                                border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                                padding-top: 1px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px; 
                                width: 100%; height: 40px;">
    <h5 class="card-title" style="background-color:#4169E1; color:#F5F5F5; font-family:sans-serif;
                                  padding-top: 7px; padding-right: 15px; padding-bottom: 1px; padding-left: 15px; 
                                  text-align: center;font-size: 100%;" 
                                  >Palavras mais frequêntes nas Descrições</h5>
  </div>
</div>
"""

html_card_header_CC="""
<div class="card">
  <div class="card-body" style="border-radius: 15px 15px 0px 0px; background: #4169E1;  
                                border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                                padding-top: 1px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px; 
                                width: 100%; height: 40px;">
    <h5 class="card-title" style="background-color:#4169E1; color:#F5F5F5; font-family:sans-serif;
                                  padding-top: 7px; padding-right: 15px; padding-bottom: 1px; padding-left: 15px; 
                                  text-align: center;font-size: 120%;" 
                                  >Publicações por Turno e Dia da Semana</h5>
  </div>
</div>
"""



#-------------------------------------------------------------------------------------------------------
html_card_header_3A1="""
<div class="card">
  <div class="card-body" style="border-radius: 15px 15px 0px 0px; background: #4169E1;  
                                border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                                padding-top: 1px; padding-right: 20px; padding-bottom: 1px; padding-left: 20px; 
                                width: 100%; height: 40px;">
    <h5 class="card-title" style="background-color:#4169E1; color:#F5F5F5; font-family:sans-serif;
                                  padding-top: 7px; padding-right: 15px; padding-bottom: 1px; padding-left: 15px; 
                                  text-align: center;font-size: 120%;" 
                                  >Tabela Interativa</h5>
  </div>
</div>
"""