import streamlit as st

st.set_page_config(page_title="DI CHECK - Auditoria TikTok/Shopee", layout="wide")

st.title("🛡️ DI CHECK - Sistema de Auditoria Ativo")
st.write("O sistema está online e operando com rigor geométrico total.")

# Definindo o prompt unificado de forma segura
SYSTEM_PROMPT_DI_CHECK = (
    "Você é o DI CHECK, um sistema especialista avançado de inteligência artificial, "
    "atuando como o auditor sênior de conformidade, segurança e inteligência regulatória "
    "para vídeos de criadores e afiliados voltados para e-commerce e plataformas de alta performance (como TikTok Shop e Shopee)."
)

st.success("Prompt carregado com sucesso sem erros de sintaxe!")
