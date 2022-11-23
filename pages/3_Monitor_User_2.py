from layout.teste_pages3 import *


st.markdown("# Insta Monitor User 2 ")
st.sidebar.markdown("# Insta Monitor User 2")

tab1, tab2, tab3 = st.tabs(["Monitor de Publicaçôes", "Monitor de Comentários", "Tabela Interativa"])
with tab1:
    parte1()
with tab2:
    parte1()
with tab3:
    parte1()

rodape()