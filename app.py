import streamlit as st
from google import genai
import os
import time

# Configuração da página do aplicativo
st.set_page_config(
    page_title="DI CHECK - Auditoria de Vídeos",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ DI CHECK - Auditoria Inteligente")
st.subheader("Análise de Vídeos para TikTok Shop e Shopee")
st.write("O sistema analisa o vídeo enviado para caçar falhas visuais, logotipos incorretos e riscos de rejeição.")

st.divider()

# Configuração da Chave da API
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 **Chave da API do Gemini não encontrada!** Adicione a chave nos *Secrets* do Streamlit Cloud.")
else:
    client = genai.Client(api_key=api_key)

    # 1. Área de Upload de Vídeo
    st.markdown("### 1. Enviar Vídeo para Auditoria")
    video_carregado = st.file_uploader(
        "Selecione o ficheiro de vídeo (.mp4, .mov, .avi)", 
        type=["mp4", "mov", "avi", "mkv"]
    )

    if video_carregado is not None:
        st.success("Vídeo carregado com sucesso!")
        st.video(video_carregado)
        
        st.divider()
        
        # Botão para iniciar a auditoria
        if st.button("🚀 Executar Auditoria de Vídeo", type="primary"):
            with st.spinner("A IA está a processar e a inspecionar o vídeo detalhadamente..."):
                try:
                    # Guarda o vídeo temporariamente
                    with open("temp_video.mp4", "wb") as f:
                        f.write(video_carregado.getbuffer())

                    # Faz o upload do ficheiro para a API do Google
                    video_file = client.files.upload(file="temp_video.mp4")
                    
                    # Aguarda o processamento completo do ficheiro na nuvem
                    while video_file.state.name == "PROCESSING":
                        time.sleep(2)
                        video_file = client.files.get(name=video_file.name)

                    # Prompt analítico profundo e incisivo para detetar anomalias visuais
                    prompt_auditoria = (
                        "Você é um auditor sênior de conformidade, qualidade e segurança de contas para o TikTok Shop e Shopee. "
                        "Analise este vídeo quadro a quadro com máximo rigor. "
                        "Procure ativamente por qualquer anomalia ou defeito visual: "
                        "1. Verifique se existem logotipos, marcas ou estampas impressas ou visíveis na parte de trás de produtos (como bolsas, mochilas ou roupas) onde no produto original ou correto elas NÃO deveriam existir. "
                        "2. Identifique qualquer inconsistência estrutural, defeito de fabricação aparente ou divergência com padrões reais de e-commerce. "
                        "3. Avalie se o vídeo apresenta risco de rejeição pelos robôs das plataformas ou banimento de conta. "
                        "FORMATO OBRIGATÓRIO DE RESPOSTA: "
                        "- Comece obrigatoriamente com o veredicto: [APROVADO] ou [REPROVADO]. "
                        "- Em seguida, elabore um relatório detalhado apontando exatamente quais falhas, logotipos indevidos ou riscos foram encontrados na gravação."
                    )

                    # Chamada limpa passando o objeto do ficheiro de vídeo e o texto diretamente
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=[video_file, prompt_auditoria]
                    )

                    # Exibe o relatório gerado pela IA
                    st.markdown("### 📋 Relatório de Auditoria")
                    
                    texto_resposta = response.text
                    
                    if "[REPROVADO]" in texto_resposta.upper() or "RISCO" in texto_resposta.upper() or "FALHA" in texto_resposta.upper():
                        st.error("🚨 **VEREDICTO: REPROVADO / RISCO DETETADO**")
                    else:
                        st.success("✅ **VEREDICTO: APROVADO**")
                        
                    st.write(texto_resposta)

                    # Limpeza do ficheiro temporário local
                    os.remove("temp_video.mp4")

                except Exception as e:
                    st.error(f"Ocorreu um erro durante o processamento: {e}")
    else:
        st.info("ℹ️ Faça o upload de um vídeo acima para iniciar a auditoria.")
