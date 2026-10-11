import streamlit as st
from google import genai
import os
import time

# Configuração da página do aplicativo
st.set_page_config(
    page_title="DI CHECK - Auditoria por Checklist",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ DI CHECK - Auditoria Inteligente")
st.subheader("Análise de Conformidade para TikTok Shop e Shopee")
st.write("O sistema realiza uma checklist visual detalhada para garantir segurança total antes da publicação.")

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
        if st.button("🚀 Executar Auditoria com Checklist", type="primary"):
            with st.spinner("A IA está a inspecionar o vídeo e a montar a checklist de conformidade..."):
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

                    # Prompt estruturado para gerar a checklist com ✅ / ❌ e a lógica de veredicto
                    prompt_auditoria = (
                        "Você é um auditor sênior de conformidade e segurança de contas para o TikTok Shop e Shopee. "
                        "Analise este vídeo quadro a quadro com máximo rigor. "
                        "Você deve gerar obrigatoriamente uma **Checklist de Inspeção Detalhada**, avaliando os seguintes pontos com os símbolos corretos: "
                        "- Use **✅** se o item estiver perfeito e em total conformidade. "
                        "- Use **❌** se encontrar qualquer anomalia, erro, inversão, logotipos indevidos na parte traseira de produtos (ex: bolsas/peças) ou risco. "
                        "\n\n"
                        "Itens obrigatórios da Checklist a avaliar:\n"
                        "1. **Logotipos e Estampas (Frente e Verso):** Verificação de marcas indevidas ou ausência de logotipos onde não deveriam existir.\n"
                        "2. **Padrão de Produto Original:** Conformidade estrutural e visual com o mercado oficial.\n"
                        "3. **Riscos de Moderação (Robôs da Plataforma):** Inspecionando elementos que possam gerar penalização, queda de score ou banimento.\n"
                        "\n"
                        "REGRAS RÍGIDAS DE AVALIAÇÃO:\n"
                        "- Se houver **pelo menos um** item marcado com ❌, o veredicto final DEVE ser obrigatoriamente **[REPROVADO]** e você deve explicar o motivo exato logo abaixo.\n"
                        "- O vídeo só poderá receber o veredicto **[APROVADO]** se e somente se **todos** os itens da checklist estiverem marcados com ✅."
                    )

                    # Mecanismo de tentativas automáticas caso o servidor esteja com alta procura (503)
                    max_tentativas = 3
                    sucesso = False
                    response = None

                    for tentativa in range(max_tentativas):
                        try:
                            response = client.models.generate_content(
                                model='gemini-3.8-flash',
                                contents=[video_file, prompt_auditoria]
                            )
                            sucesso = True
                            break
                        except Exception as err:
                            if "503" in str(err) and tentativa < max_tentativas - 1:
                                time.sleep(5)
                            else:
                                raise err

                    if sucesso and response:
                        # Exibe o relatório gerado pela IA
                        st.markdown("### 📋 Relatório de Auditoria (Checklist)")
                        
                        texto_resposta = response.text
                        
                        # Verifica o veredicto baseado na resposta da IA
                        if "[REPROVADO]" in texto_resposta.upper() or "❌" in texto_resposta:
                            st.error("🚨 **VEREDICTO FINAL: REPROVADO (CONTÉM FALHAS / NÃO PUBLIQUE)**")
                        else:
                            st.success("✅ **VEREDICTO FINAL: APROVADO PARA PUBLICAÇÃO**")
                            
                        st.write(texto_resposta)

                    # Limpeza do ficheiro temporário local
                    os.remove("temp_video.mp4")

                except Exception as e:
                    st.error(f"Ocorreu um erro durante o processamento: {e}")
    else:
        st.info("ℹ️ Faça o upload de um vídeo acima para iniciar a auditoria.")
