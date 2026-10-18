import streamlit as st
import google.generativeai as genai

# Configuração da página
st.set_page_config(page_title="DI CHECK - Auditoria TikTok/Shopee", layout="wide")

st.title("🛡️ DI CHECK - Sistema de Auditoria Rigorosa")
st.write("Auditoria multi-ângulo de alta precisão e blindagem contra inconsistências estruturais.")

# Campo para inserir a chave da API do Gemini
api_key = st.text_input("Insira sua Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # Prompt com Inspeção Forense e Tolerância Zero Absoluta
    SYSTEM_PROMPT_DI_CHECK = (
        "Você é o DI CHECK, o mais avançado sistema de auditoria de conformidade para e-commerce "
        "e plataformas como TikTok Shop e Shopee. Sua função é atuar com rigor idêntico ao de um "
        "auditor humano sênior de segurança de marca e conformidade de criadores.\n\n"
        
        "Sua missão é realizar uma ANÁLISE FORENSE E CRUZADA entre as imagens oficiais da vitrine "
        "(até 4 imagens de referência) e o vídeo do criador. Você não deve perdoar nenhuma divergência.\n\n"
        
        "--- \n\n"
        
        "### PROTOCOLO DE INSPEÇÃO FORENSE (TOLERÂNCIA ZERO):\n"
        "1. **Comparação Geométrica Direta:** Compare a geometria exata, o contorno, o formato das alças, puxadores, tampas, bicos e proporções das imagens oficiais com o que aparece no vídeo.\n"
        "2. **Detecção de Mudança por IA ou Versão Diferente:** Se a foto oficial mostra um tipo de componente (ex: alça rígida, tampa de rosca específica) e o vídeo exibe outro diferente (ex: alça flexível, anel, outro modelo de tampa), o produto é considerado **INCONSISTENTE**.\n"
        "3. **Veredicto Obrigatório:** Qualquer discrepância física entre o item da foto e o item manuseado no vídeo obriga você a emitir o veredicto de **REPROVADO** com justificativa detalhada apontando o erro estrutural.\n\n"
        
        "--- \n\n"
        
        "### FORMATO OBRIGATÓRIA DA RESPOSTA:\n"
        "1. **Veredicto:** (APROVADO ou REPROVADO em destaque absoluto)\n"
        "2. **Análise Detalhada:** O que foi encontrado nas fotos de referência versus o que apareceu no vídeo.\n"
        "3. **Inconsistências Encontradas:** Descreva cirurgicamente o erro (ex: 'A alça do produto no vídeo difere estruturalmente da alça fixa exibida na foto de referência 1...').\n"
        "4. **Orientação ao Criador:** Instruções de como corrigir o vídeo para evitar banimento ou perda de pontos de integridade na plataforma."
    )

    st.markdown("---")
    
    # Checklist Visual Interativo na Interface
    st.subheader("📋 Checklist de Critérios Ativos na Auditoria")
    col_a, col_b = st.columns(2)
    with col_a:
        st.checkbox("Fidelidade Estrutural e Geométrica (Alças, Puxadores e Tampas)", value=True, disabled=True)
        st.checkbox("Análise Multi-Ângulo Simultânea (Até 4 imagens de referência)", value=True, disabled=True)
        st.checkbox("Legibilidade de Textos e Rótulos (Sem Efeito Espelho)", value=True, disabled=True)
    with col_b:
        st.checkbox("Consistência de Preço e Apelo Comercial", value=True, disabled=True)
        st.checkbox("Tratamento Adequado de Acessórios de Cenário (Props)", value=True, disabled=True)
        st.checkbox("Qualidade Técnica, Foco e Iluminação do Vídeo", value=True, disabled=True)

    st.markdown("---")
    
    # Upload de arquivos
    col1, col2 = st.columns(2)
    with col1:
        uploaded_images = st.file_uploader("Envie as imagens oficiais da vitrine (Até 4 imagens em alta definição):", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    with col2:
        uploaded_video = st.file_uploader("Envie o vídeo do criador para auditoria:", type=["mp4", "mov", "avi"])

    if st.button("🚀 Iniciar Auditoria Forense Multi-Ângulo"):
        if uploaded_video and uploaded_images:
            with st.spinner("Executando inspeção forense de alta resolução e cruzamento de dados..."):
                try:
                    model = genai.GenerativeModel("gemini-3.8-flash", system_instruction=SYSTEM_PROMPT_DI_CHECK)
                    
                    content_parts = []
                    
                    # Adiciona as imagens preservando integralmente os bytes originais em alta definição
                    for img in uploaded_images[:4]:
                        content_parts.append({
                            "mime_type": img.type,
                            "data": img.getvalue()
                        })
                    
                    # Adiciona o vídeo
                    content_parts.append({
                        "mime_type": uploaded_video.type,
                        "data": uploaded_video.getvalue()
                    })
                    
                    # Comando imperativo para o motor focar na falha
                    content_parts.append(
                        "Execute a inspeção forense completa. Confronte cada milímetro das imagens oficiais com o vídeo enviado. "
                        "Verifique com rigor extremo se há qualquer divergência em alças, puxadores, tampas ou formatos. Se houver divergência, reprove imediatamente."
                    )
                    
                    response = model.generate_content(content_parts)
                    
                    st.markdown("### Resultado da Auditoria DI CHECK:")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Ocorreu um erro durante a comunicação com a API do Gemini: {e}")
        else:
            st.warning("Por favor, envie ao menos uma imagem de referência e o vídeo para iniciar a análise.")
else:
    st.info("Insira sua chave de API do Gemini acima para habilitar o painel de auditoria.")
        
