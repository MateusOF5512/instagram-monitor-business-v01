from layout.pages_brasil2 import *


st.markdown("# Insta Monitor User 1")
st.sidebar.markdown("# Insta Monitor User 1")

tab1, tab2, tab3 = st.tabs(["Monitor de Publicaçôes", "Monitor de Comentários", "Tabela Interativa"])
with tab1:
    brasil1()
with tab2:
    comentarios()
with tab3:
    brasil1()

rodape()