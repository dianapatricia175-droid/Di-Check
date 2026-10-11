import streamlit as st
from google import genai
import os
import time

# Configuração da página do aplicativo
st.set_page_config(
    page_title="DI CHECK - Auditoria Autónoma",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 DI CHECK - Auditoria Autónoma por IA")
st.subheader("Varredura Inteligente e Deteção de Anomalias (TikTok & Shopee)")
st.write("O sistema navega autonomamente pelo vídeo para caçar falhas ocultas, logotipos invertidos e riscos de rejeição.")

st.divider()

# Configuração da Chave da API
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 **Chave da API do Gemini não encontrada!** Adicione a chave nos *Secrets* do Streamlit Cloud.")
else:
    client = genai.Client(api_key=api_key)

    # 1. Área de Upload de Vídeo
    st.markdown("### 1. Enviar Vídeo para Varredura")
    video_carregado = st.file_uploader(
        "Selecione o ficheiro de vídeo (.mp4, .mov, .avi)", 
        type=["mp4", "mov", "avi", "mkv"]
    )

    if video_carregado is not None:
        st.success("Vídeo carregado com sucesso!")
        st.video(video_carregado)
        
        st.divider()
        
        # Botão para iniciar a varredura autónoma
        if st.button("🚀 Executar Varredura Autónoma Profunda", type="primary"):
            with st.spinner("A IA está a navegar autonomamente pelo vídeo e a inspecionar os detalhes visuais..."):
                try:
                    # Guarda o vídeo temporariamente
                    with open("temp_video.mp4", "wb") as f:
                        f.write(video_carregado.getbuffer())

                    # Faz o upload do ficheiro para a API
                    video_file = client.files.upload(file="temp_video.mp4")
                    
                    # Aguarda o processamento completo do ficheiro na nuvem do Google
                    while video_file.state.name == "PROCESSING":
                        time.sleep(2)
                        video_file = client.files.get(name=video_file.name)

                    # Prompt totalmente autónomo exigindo caça ativa de anomalias e padrão de mercado
                    prompt_auditoria = (
                        "Você é um sistema automatizado de controlo de qualidade e conformidade implacável para e-commerce (TikTok Shop e Shopee). "
                        "Analise este vídeo de forma totalmente autónoma. O seu objetivo é encontrar QUALQUER anomalia, defeito visual, inversão de logotipos (ex: marcas impressas onde não deveriam existir no produto original), "
                        "inconsistências de design frente/verso, ou elementos que possam desencadear penalizações de conta ou rejeição pelos robôs de moderação. "
                        "Não espere que o utilizador aponte os erros: investigue ativamente o produto exibido quadro a quadro, compare com o padrão real de fabricação desse tipo de item e aponte com precisão cirúrgica o que está errado. "
                        "FORMATO OBRIGATÓRIO: "
                        "1. Veredicto: [APROVADO] ou [REPROVADO]. "
                        "2. Anomalias Detetadas (indique o momento/timestamp se aplicável e o erro exato detetado)."
                    )

                    # Chamada ao modelo utilizando o modo Agentic para máxima precisão visual em movimento
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=[
                            {
                                "type": "video",
                                "file_uri": video_file.uri,
                                "processing": "agentic"  # Ativa a navegação autónoma e inteligente na timeline
                            },
                            prompt_auditoria
                        ]
                    )

                    # Exibe o relatório gerado pela IA
                    st.markdown("### 📋 Relatório de Auditoria Autónoma")
                    
                    texto_resposta = response.text
                    
                    if "[REPROVADO]" in texto_resposta.upper() or "ERRO" in texto_resposta.upper() or "ANOMALIA" in texto_resposta.upper():
                        st.error("🚨 **VEREDICTO: REPROVADO (RISCO ENCONTRADO)**")
                    else:
                        st.success("✅ **VEREDICTO: APROVADO**")
                        
                    st.write(texto_resposta)

                    # Limpeza do ficheiro temporário local
                    os.remove("temp_video.mp4")

                except Exception as e:
                    st.error(f"Ocorreu um erro durante a varredura autónoma: {e}")
    else:
        st.info("ℹ️ Faça o upload de um vídeo acima para iniciar a auditoria autónoma.")
