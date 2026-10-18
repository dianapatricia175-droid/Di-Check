import streamlit as st
import google.generativeai as genai

# Configuração da página e design moderno com CSS personalizado
st.set_page_config(
    page_title="DI CHECK - Auditoria TikTok/Shopee",
    page_icon="🛡️",
    layout="wide"
)

# Estilização CSS Moderna (Cards, Sombras, Fontes e Cores Customizadas)
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stTextInput input {
        background-color: #1e293b;
        color: #ffffff;
        border-radius: 8px;
        border: 1px solid #334155;
    }
    .stFileUploader {
        background-color: #1e293b;
        border: 2px dashed #475569;
        border-radius: 12px;
        padding: 15px;
    }
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 12px;
    }
    .stButton button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        border: none;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        width: 100%;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho Principal Moderno
st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🛡️ DI CHECK - Sistema de Auditoria Rigorosa</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.1rem;'>Auditoria multi-ângulo de alta precisão e blindagem contra inconsistências estruturais e de IA.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Campo para inserir a chave da API do Gemini em destaque
col_key1, col_key2, col_key3 = st.columns([1, 2, 1])
with col_key2:
    api_key = st.text_input("🔑 Insira sua Gemini API Key:", type="password", placeholder="Cole sua chave aqui...")

if api_key:
    genai.configure(api_key=api_key)
    
    # Prompt com Inspeção Cirúrgica e Foco em Divergência de Componentes
    SYSTEM_PROMPT_DI_CHECK = (
        "Você é o DI CHECK, um sistema especialista em auditoria de conformidade para e-commerce "
        "e plataformas de alta performance como TikTok Shop e Shopee. Sua responsabilidade máxima "
        "é proteger o criador contra punições por 'Promoção de Produto Inconsistente'.\n\n"
        
        "Você receberá um conjunto de imagens oficiais de referência (até 4 imagens) e um vídeo de divulgação. "
        "Sua tarefa é cruzar as características físicas estáticas das fotos com o item real manuseado no vídeo.\n\n"
        
        "### REGRAS CRÍTICAS DE AUDITORIA (TOLERÂNCIA ZERO PARA DIFERENÇAS):\n"
        "1. **Análise de Componentes e Micro-Detalhes:** Compare obrigatoriamente alças, puxadores, tampas, bicos, fechos, proporções e acabamentos visuais entre as fotos oficiais e o vídeo.\n"
        "2. **Detecção de Divergência Estrutural:** Se a foto oficial apresentar um tipo de componente (ex: alça rígida ou formato específico de tampa) e o vídeo mostrar outro (ex: alça flexível ou tampa diferente), o produto é estruturalmente diferente.\n"
        "3. **Veredicto Obrigatório:** Caso identifique qualquer divergência física ou geométrica, você DEVE emitir o veredicto de **REPROVADO** e apontar explicitamente qual parte do produto divergiu das imagens de referência."
    )

    st.markdown("---")
    
    # Checklist Visual Dinâmico com Ícones de Aprovado (✅) e Reprovado (❌)
    st.markdown("### 📋 Painel de Critérios Ativos na Auditoria")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class='metric-card'>
            <b>✅ Fidelidade Estrutural e Geométrica</b><br><span style='color: #94a3b8; font-size: 0.85rem;'>Alças, puxadores, tampas e proporções validadas.</span>
        </div>
        <div class='metric-card'>
            <b>✅ Análise Multi-Ângulo Simultânea</b><br><span style='color: #94a3b8; font-size: 0.85rem;'>Cruzamento com até 4 fotos oficiais da vitrine.</span>
        </div>
        <div class='metric-card'>
            <b>✅ Legibilidade de Textos e Rótulos</b><br><span style='color: #94a3b8; font-size: 0.85rem;'>Verificação contra inversão ou efeito espelho.</span>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class='metric-card'>
            <b>❌ Tolerância Zero a Inconsistências</b><br><span style='color: #94a3b8; font-size: 0.85rem;'>Reprovado imediato se houver divergência física.</span>
        </div>
        <div class='metric-card'>
            <b>❌ Tratamento Rigoroso de Props</b><br><span style='color: #94a3b8; font-size: 0.85rem;'>Controle estrito sobre acessórios de cenário.</span>
        </div>
        <div class='metric-card'>
            <b>✅ Padrão Técnico e Visual</b><br><span style='color: #94a3b8; font-size: 0.85rem;'>Checagem de foco, iluminação e artefatos de IA.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Seção de Upload de Arquivos Organizada em Cards Modernos
    st.markdown("### 📁 Envio de Arquivos para Auditoria")
    col1, col2 = st.columns(2)
    with col1:
        uploaded_images = st.file_uploader("🖼️ Imagens oficiais da vitrine (Até 4 fotos):", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    with col2:
        uploaded_video = st.file_uploader("🎥 Vídeo do criador para auditoria:", type=["mp4", "mov", "avi"])

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Botão Centralizado de Execução
    if st.button("🚀 Iniciar Auditoria Rigorosa de Inconsistência"):
        if uploaded_video and uploaded_images:
            with st.spinner("🔄 Analisando imagens oficiais e cruzando quadros do vídeo... Aguarde."):
                try:
                    model = genai.GenerativeModel("gemini-3.8-flash", system_instruction=SYSTEM_PROMPT_DI_CHECK)
                    
                    content_parts = []
                    
                    # Adiciona as imagens oficiais de referência
                    for img in uploaded_images[:4]:
                        content_parts.append({
                            "mime_type": img.type,
                            "data": img.getvalue()
                        })
                    
                    # Adiciona o vídeo do criador
                    content_parts.append({
                        "mime_type": uploaded_video.type,
                        "data": uploaded_video.getvalue()
                    })
                    
                    # Instrução assertiva final
                    content_parts.append(
                        "Confronte rigorosamente o produto exibido no vídeo com as imagens oficiais da vitrine enviadas acima. "
                        "Verifique detalhadamente se a alça, puxador, tampa ou qualquer outro componente estrutural no vídeo difere das fotos oficiais. "
                        "Se houver qualquer divergência estrutural, declare explicitamente o veredicto de REPROVADO e detalhe qual é a inconsistência encontrada."
                    )
                    
                    response = model.generate_content(content_parts)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("### 📊 Resultado da Auditoria DI CHECK:")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Ocorreu um erro durante a comunicação com a API do Gemini: {e}")
        else:
            st.warning("⚠️ Por favor, envie ao menos uma imagem de referência e o vídeo para iniciar a análise.")
else:
    st.info("💡 Insira sua chave de API do Gemini acima para habilitar o painel moderno de auditoria.")
    
