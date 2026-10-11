import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="DI CHECK",
    page_icon="✅",
    layout="centered"
)

# Título principal do aplicativo
st.title("✅ DI CHECK")
st.write("Bem-vindo ao seu aplicativo de verificação e gestão de tarefas/dados!")

st.divider()

# Exemplo de conteúdo interativo para testar se tudo está a funcionar
st.subheader("Painel de Controlo")

nome_utilizador = st.text_input("Insira o seu nome:")

if nome_utilizador:
    st.success(f"Olá, {nome_utilizador}! O aplicativo está a funcionar perfeitamente.")

# Secção de verificação rápida
st.markdown("### Lista de Verificação Rápida")
tarefa_1 = st.checkbox("Verificar dados inseridos")
tarefa_2 = st.checkbox("Validar configuração no Streamlit Cloud")
tarefa_3 = st.checkbox("Testar aplicação no telemóvel")

if all([tarefa_1, tarefa_2, tarefa_3]):
    st.balloons()
    st.success("Parabéns! Todas as etapas foram concluídas com sucesso!")
else:
    st.info("Complete os itens acima para finalizar o processo.")

