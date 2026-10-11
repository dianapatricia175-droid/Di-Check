import streamlit as st
from google import genai
import os

# Configuração da página do aplicativo
st.set_page_config(
    page_title="DI CHECK - Auditoria com IA",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 DI CHECK - Auditoria Inteligente")
st.subheader("Análise Avançada de Vídeos para TikTok Shop e Shopee")
st.write("O sistema utiliza Inteligência Artificial para inspecionar o vídeo e detetar inconsistências visuais, logotipos incorretos e produtos restritos.")

st.divider()

# Configuração da Chave da API do Gemini de forma segura
# (O Streamlit busca a chave automaticamente nos "Secrets" do painel)
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 **Chave da API do Gemini não encontrada!** Por favor, adicione a chave nas configurações (Secrets) do seu projeto no Streamlit Cloud.")
else:
    # Inicializa o cliente oficial do Google GenAI
    client = genai.Client(api_key=api_key)

    # 1. Área de Upload de Vídeo
    st.markdown("### 1. Carregar Vídeo para Análise Automática")
    video_carregado = st.file_uploader(
        "Selecione o ficheiro de vídeo (.mp4, .mov, .avi)", 
        type=["mp4", "mov", "avi", "mkv"]
    )

    if video_carregado is not None:
        st.success("Ficheiro carregado com sucesso!")
        st.video(video_carregado)
        
        st.divider()
        
        # Botão para iniciar a análise por IA
        if st.button("🚀 Iniciar Auditoria de IA", type="primary"):
            with st.spinner("A IA está a analisar o vídeo quadro a quadro em busca de inconsistências e riscos..."):
                try:
                    # Salva temporariamente o vídeo carregado para envio à API
                    with open("temp_video.mp4", "wb") as f:
                        f.write(video_carregado.getbuffer())

                    # Envia o vídeo para o Gemini processar o ficheiro multimédia
                    video_file = client.files.upload(file="temp_video.mp4")
                    
                    # Prompt focado nas regras exigidas para o TikTok Shop e Shopee
                    prompt_auditoria = (
                        "Você é um auditor especialista em conformidade para o TikTok Shop e Shopee. "
                        "Analise este vídeo detalhadamente. Verifique: "
                        "1. Se existem inconsistências visuais graves, como logotipos de marcas aparecendo incorretamente onde não deveriam (ex: marca no verso de uma bolsa onde não existe no original). "
                        "2. Se há presença de produtos proibidos, restritos ou falsificados. "
                        "3. Se o conteúdo pode gerar penalizações ou banimento de conta. "
                        "Forneça um relatório claro indicando se o vídeo está APROVADO ou se contém RISCO DE PENALIZAÇÃO, detalhando os motivos."
                    )

                    # Chamada ao modelo multimodal do Gemini
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[video_file, prompt_auditoria]
                    )

                    # Exibe o resultado da auditoria da IA
                    st.markdown("### 📋 Relatório de Auditoria da IA")
                    st.write(response.text)

                    # Limpeza do ficheiro temporário local
                    os.remove("temp_video.mp4")

                except Exception as e:
                    st.error(f"Ocorreu um erro durante o processamento com a IA: {e}")
    else:
        st.info("ℹ️ Faça o upload de um vídeo acima para começar a auditoria automática.")
