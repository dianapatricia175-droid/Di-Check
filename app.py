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
            status_box = st.status("A iniciar processo...", expanded=True)
            
            try:
                status_box.update(label="A guardar o ficheiro temporariamente...", state="running")
                with open("temp_video.mp4", "wb") as f:
                    f.write(video_carregado.getbuffer())

                status_box.update(label="A enviar o vídeo para a nuvem da Google...", state="running")
                video_file = client.files.upload(file="temp_video.mp4")
                
                status_box.update(label="A aguardar o processamento do vídeo na nuvem...", state="running")
                while video_file.state.name == "PROCESSING":
                    time.sleep(3)
                    video_file = client.files.get(name=video_file.name)
                    if video_file.state.name == "FAILED":
                        raise Exception("O processamento do vídeo falhou nos servidores da Google.")

                status_box.update(label="A executar a auditoria de precisão com IA...", state="running")

                # Prompt refinado para eliminar falsos positivos de marcas e validar variações de cores/modelos
                prompt_auditoria = (
                    "Você é um auditor sênior de conformidade, qualidade visual e segurança de contas para o TikTok Shop e Shopee. "
                    "Analise este vídeo quadro a quadro com rigor absoluto e sem ambiguidades. "
                    "Você deve gerar obrigatoriamente uma **Checklist de Inspeção Detalhada**, avaliando os seguintes pontos com os símbolos corretos: "
                    "- Use **✅** se o item estiver perfeito e em total conformidade. "
                    "- Use **❌** se encontrar uma anomalia real, logotipos falsificados de terceiros (marcas concorrentes indevidas) ou perda grave de nitidez / textos ilegíveis. "
                    "\n\n"
                    "Itens obrigatórios da Checklist a avaliar:\n"
                    "1. **Autenticidade de Logotipos e Marcas:** Verifique se existem marcas concorrentes ou logotipos de terceiros não autorizados. Nota importante: Exiba ✅ se o logotipo apresentado pertencer legitimamente ao produto anunciado (marcas próprias ou oficiais do lojista), sem falsos positivos.\n"
                    "2. **Nitidez e Legibilidade de Textos e Rótulos:** Os textos descritivos e especificações nas embalagens estão legíveis, ou apresentam borrões graves gerados por ferramentas de automação/Flow?\n"
                    "3. **Variações de Cores, Modelos e Linhas de Produtos:** Avalie se há múltiplas versões, cores ou potes exibidos no vídeo. **REGRA DE OURO:** A apresentação de variações de cores, sabores ou modelos lado a lado é uma prática comercial legítima e ESPERADA no e-commerce. Nunca considere variações de cores/modelos como erro ou inconsistência estrutural (atribua ✅).\n"
                    "4. **Riscos de Moderação (Robôs da Plataforma):** Inspecionando elementos que possam gerar penalização real pelas regras do marketplace.\n"
                    "\n"
                    "REGRAS RÍGIDAS DE AVALIAÇÃO:\n"
                    "- Se houver **pelo menos um** erro real marcado com ❌, o veredicto final DEVE ser obrigatoriamente **[REPROVADO]** com a explicação detalhada.\n"
                    "- O vídeo só poderá receber o veredicto **[APROVADO]** se e somente se todos os itens essenciais estiverem marcados com ✅."
                )

                modelos_para_tentar = ['gemini-3.8-flash', 'gemini-2.5-flash']
                sucesso = False
                response = None
                ultimo_erro = None

                for modelo in modelos_para_tentar:
                    for tentativa in range(2):
                        try:
                            response = client.models.generate_content(
                                model=modelo,
                                contents=[video_file, prompt_auditoria]
                            )
                            if response and hasattr(response, 'text') and response.text:
                                sucesso = True
                                break
                        except Exception as err:
                            ultimo_erro = err
                            time.sleep(3)
                    if sucesso:
                        break

                if sucesso and response and response.text:
                    status_box.update(label="Auditoria concluída com sucesso!", state="complete", expanded=False)
                    
                    st.markdown("### 📋 Relatório de Auditoria (Checklist)")
                    
                    texto_resposta = response.text
                    
                    if "[REPROVADO]" in texto_resposta.upper() or "❌" in texto_resposta:
                        st.error("🚨 **VEREDICTO FINAL: REPROVADO (CONTÉM FALHAS / NÃO PUBLIQUE)**")
                    else:
                        st.success("✅ **VEREDICTO FINAL: APROVADO PARA PUBLICAÇÃO**")
                        
                    st.write(texto_resposta)
                else:
                    status_box.update(label="Falha na resposta da IA", state="error")
                    st.error(f"Os servidores não retornaram resposta válida. Erro técnico: {ultimo_erro}")

                if os.path.exists("temp_video.mp4"):
                    os.remove("temp_video.mp4")

            except Exception as e:
                status_box.update(label="Erro crítico no processo", state="error")
                st.error(f"Ocorreu um erro durante o processamento: {e}")
                if os.path.exists("temp_video.mp4"):
                    os.remove("temp_video.mp4")
    else:
        st.info("ℹ️ Faça o upload de um vídeo acima para iniciar a auditoria.")
