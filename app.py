import streamlit as st
from google import genai
from google.genai import types

# Configuração da página e design moderno com CSS personalizado
st.set_page_config(
    page_title="DI CHECK - Auditoria TikTok/Shopee",
    page_icon="🛡️",
    layout="wide"
)

# Estilização CSS Moderna (Dark Mode SaaS)
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
        background: linear-gradient(135deg, #1d4ed8 100%, #1e40af 100%);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho Principal (Resumo básico do sistema)
st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🛡️ DI CHECK - Sistema de Auditoria Rigorosa</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.1rem;'>Auditoria automática e universal para e-commerce (TikTok Shop e Shopee) focada em conformidade, marcas, falsificações, logotipos de terceiros e integridade estrutural.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Campo para inserir a chave da API do Gemini
col_key1, col_key2, col_key3 = st.columns([1, 2, 1])
with col_key2:
    api_key = st.text_input("🔑 Insira sua Gemini API Key:", type="password", placeholder="Cole sua chave aqui...")

if api_key:
    # Inicializa o cliente oficial moderno do Google GenAI
    client = genai.Client(api_key=api_key)
    
    SYSTEM_PROMPT_DI_CHECK = (
        "Você é o DI CHECK, o sistema especialista sênior definitivo em auditoria de conformidade, segurança de marca "
        "e inteligência regulatória para vídeos de criadores no TikTok Shop e na Shopee.\n\n"
        
        "Sua missão é realizar uma ANÁLISE FORENSE CRUZADA EXAUSTIVA entre as imagens oficiais de referência da vitrine "
        "e o vídeo de divulgação enviado, aplicando rigor idêntico (ou superior) ao dos robôs de moderação automatizada das plataformas.\n\n"
        
        "### DIRETRIZES DE AUDITORIA COMPLETA E TOLERÂNCIA ZERO (TODOS OS ASPECTOS EXIGIDOS):\n"
        "1. **Detecção de Logotipos e Marcas d'Água de Terceiros (Anti-Watermark / Vídeo Roubado):**\n"
        "   - Inspecione minuciosamente se o vídeo exibe logotipos, marcas d'água, @s, nomes de perfis ou identidades visuais de outros criadores, lojas concorrentes ou plataformas externas. Caso o vídeo pertença a terceiros, a infração é gravíssima.\n"
        "2. **Verificação de Marcas, Falsificações e Imitações (Anti-Counterfeit & IP Policy):**\n"
        "   - Inspecione se há comercialização de produtos falsificados, imitações, réplicas, produtos 'inspirados em' ou cópias não autorizadas que infrinjam marcas registradas e propriedade intelectual (IP).\n"
        "3. **Fidelidade de Categoria, Modelo e Variação:**\n"
        "   - Valide se o item real manuseado no vídeo pertence exatamente à mesma categoria, subtipo, cor, design e especificações técnicas das fotos oficiais da vitrine (proibida troca oculta de produtos ou envio de versões inferiores).\n"
        "4. **Inconsistências Estruturais e Micro-Detalhes:**\n"
        "   - Confronte milimetricamente componentes físicos (alças, puxadores, tampas, bicos, acabamentos, texturas e proporções volumétricas) para detectar divergências entre a foto estática e o item real.\n"
        "5. **Conformidade de Legibilidade e Mídia:**\n"
        "   - Verifique se rótulos, inscrições e textos exibidos no vídeo estão nítidos, corretos e sem inversão incorreta (efeito espelho indesejado).\n"
        "6. **Consistência Comercial, Preço e Padrão Técnico:**\n"
        "   - Certifique-se de que a locução e o apelo promocional condizem com a oferta cadastrada, avaliando também a iluminação, nitidez e segurança do vídeo.\n\n"
        
        "### FORMATO OBRIGATÓRIO DA SUA RESPOSTA (SIGA EXATAMENTE ESTA ORDEM):\n"
        "Sua resposta DEVE começar obrigatoriamente na primeira linha com o veredicto em destaque, seguido imediatamente pelo painel de critérios completo. Não escreva nenhuma introdução antes disso:\n\n"
        "🔴 **VEREDICTO: REPROVADO** (ou 🟢 **VEREDICTO: APROVADO**)\n\n"
        "### 📋 PAINEL DE CRITÉRIOS DA AUDITORIA:\n"
        "- [✅ ou ❌] Autoria do Vídeo / Ausência de Logos de Terceiros\n"
        "- [✅ ou ❌] Autenticidade de Marca e Conformidade de IP (Sem Falsificações/Imitações)\n"
        "- [✅ ou ❌] Fidelidade de Categoria e Modelo do Produto\n"
        "- [✅ ou ❌] Integridade Estrutural e de Componentes Físicos (Alças, Tampas, etc.)\n"
        "- [✅ ou ❌] Legibilidade de Textos, Marcas e Rótulos (Sem Efeito Espelho)\n"
        "- [✅ ou ❌] Consistência Comercial, Preço e Padrão Técnico do Vídeo\n\n"
        "### 📝 RELATÓRIO TÉCNICO DETALHADO:\n"
        "(Descreva objetivamente os motivos da aprovação ou aponte cirurgicamente cada infração de logo de terceiros, marca, falsificação ou divergência estrutural encontrada que justifique a reprovação)."
    )

    st.markdown("---")
    
    # Seção de Upload de Arquivos
    st.markdown("### 📁 Envio de Arquivos para Auditoria")
    col1, col2 = st.columns(2)
    with col1:
        uploaded_images = st.file_uploader("🖼️ Imagens oficiais da vitrine (Até 4 fotos):", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    with col2:
        uploaded_video = st.file_uploader("🎥 Vídeo do criador para auditoria:", type=["mp4", "mov", "avi"])

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Botão de Execução
    if st.button("🚀 Iniciar Auditoria Completa de Conformidade"):
        if uploaded_video and uploaded_images:
            with st.spinner("🔄 Processando vídeo completo e imagens oficiais... Analisando logotipos, marcas, falsificações e estrutura. Aguarde."):
                try:
                    contents = []
                    
                    # Adiciona as imagens oficiais de referência
                    for img in uploaded_images[:4]:
                        contents.append(
                            types.Part.from_bytes(
                                data=img.getvalue(),
                                mime_type=img.type,
                            )
                        )
                    
                    # Adiciona o vídeo bruto para análise inteligente
                    contents.append(
                        types.Part.from_bytes(
                            data=uploaded_video.getvalue(),
                            mime_type=uploaded_video.type,
                        )
                    )
                    
                    # Instrução final imperativa
                    contents.append(
                        "Execute a auditoria forense completa em todo o vídeo enviado e nas imagens oficiais da vitrine. "
                        "Verifique rigorosamente se há logotipos de terceiros, indícios de produto falsificado, imitação, réplica, uso indevido de marca ou divergência estrutural. "
                        "Gere o resultado seguindo estritamente o formato exigido: comece diretamente com o Veredicto e o Painel de Critérios completos (com ✅ e ❌) logo no topo, seguido do relatório técnico."
                    )
                    
                    # Chamada utilizando o modelo moderno atualizado gemini-3.8-flash
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT_DI_CHECK,
                            temperature=0.1
                        ),
                    )
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("### 📊 Resultado da Auditoria DI CHECK:")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Ocorreu um erro durante a comunicação com a API do Gemini: {e}")
        else:
            st.warning("⚠️ Por favor, envie ao menos uma imagem de referência e o vídeo para iniciar a análise.")
else:
    st.info("💡 Insira sua chave de API do Gemini acima para habilitar o painel de auditoria.")
        
