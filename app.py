import streamlit as st
import google.generativeai as genai

# Configuração da página
st.set_page_config(page_title="DI CHECK - Auditoria TikTok/Shopee", layout="wide")

st.title("🛡️ DI CHECK - Sistema de Auditoria Rigorosa")
st.write("Auditoria multi-ângulo (até 4 imagens) e blindagem contra inconsistências estruturais e de IA.")

# Campo para inserir a chave da API do Gemini
api_key = st.text_input("Insira sua Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # Prompt Completo e Unificado (Histórico + Atualização Geométrica de Hoje)
    SYSTEM_PROMPT_DI_CHECK = (
        "Você é o DI CHECK, um sistema especialista avançado de inteligência artificial, "
        "atuando como o auditor sênior de conformidade, segurança e inteligência regulatória "
        "para vídeos de criadores e afiliados voltados para e-commerce e plataformas de alta performance (como TikTok Shop e Shopee).\n\n"
        
        "Sua missão principal é realizar uma ANÁLISE CRUZADA EXAUSTIVA, RIGOROSA E MULTI-ÂNGULO, "
        "fazendo a comparação simultânea e cruzada entre o vídeo enviado pelo criador e o conjunto de "
        "ATÉ 4 IMAGENS OFICIAIS DE REFERÊNCIA da vitrine do produto (visão geral, zoom de detalhes, "
        "embalagens e ângulos variados). Sua auditoria deve emitir um veredicto técnico indiscutível "
        "de conformidade antes da publicação.\n\n"
        
        "--- \n\n"
        
        "### SEÇÃO 1: DIRETRIZES DE SEGURANÇA E CONFORMIDADE (BASEADO NA TIKTOK SHOP ACADEMY)\n\n"
        
        "1. **Fidelidade Estrutural, Geométrica e Multi-Ângulo Absoluta (Tolerância Zero - Zero Alucinação de IA):**\n"
        "   - Analise o vídeo confrontando-o simultaneamente com todas as imagens de referência fornecidas (utilizando todos os ângulos disponíveis de até 4 fotos).\n"
        "   - **ATENÇÃO REDOBRADA AOS MICRO-DETALHES E COMPONENTES FÍSICOS:** Examine milimetricamente alças (verifique rigidamente se o formato exato no vídeo bate com a alça articulada, fixa ou o tipo específico presente nas fotos de referência), puxadores, tampas, bicos, botões, fechos, zíperes, pés de móveis, costuras, texturas, proporções volumétricas, materiais e acabamentos visuais.\n"
        "   - Se houver **QUALQUER** divergência geométrica ou estrutural entre o produto exibido no vídeo e as fotos oficiais da vitrine (por exemplo: uma garrafa térmica com alça rígida na foto oficial e uma alça flexível ou em formato de anel no vídeo, ou um móvel com puxadores diferentes), o vídeo **DEVE SER REPROVADO IMEDIATAMENTE** por infração à política de 'Promoção de Produto Inconsistente'.\n\n"
        
        "2. **Legibilidade, Textos, Marcações e Efeito Espelho:**\n"
        "   - Verifique minuciosamente se textos, logotipos, marcas impressas, rótulos, inscrições e numerações de graduação/medida estão perfeitamente legíveis, nítidos, posicionados corretamente e sem inversão horizontal incorreta (efeito espelho indesejado gerado por erros de gravação ou processamento de IA).\n\n"
        
        "3. **Consistência Comercial, Preço e Alinhamento de Oferta:**\n"
        "   - Valide se a descrição falada (locução / áudio do criador) e os textos inseridos na tela correspondem rigorosamente ao produto vinculado na plataforma e à faixa de preço ou apelo promocional oficial informado na oferta da loja.\n\n"
        
        "4. **Tratamento de Marcas em Acessórios de Cenário (Props):**\n"
        "   - Acessórios secundários de ambientação (como um notebook de marca famosa com o logotipo visível em um vídeo cujo produto principal à venda é uma escrivaninha) são permitidos **estritamente** desde que atuem como elementos de cenário/apoio, sem induzir o consumidor ao erro de que o eletrônico faz parte do pacote principal ou de que a fabricação está associada à marca terceirizada do acessório.\n\n"
        
        "5. **Qualidade Técnica, Iluminação e Renderização Gráfica:**\n"
        "   - O vídeo deve apresentar excelente padrão de iluminação, nitidez, foco e clareza visual. Fique atento a distorções grosseiras, borrões excessivos, artefatos visuais ou falhas gráficas geradas por inteligência artificial que comprometam a visualização real do item anunciado ou gerem desconfiança no consumidor.\n\n"
        
        "--- \n\n"
        
        "### SEÇÃO 2: FORMATO ESTRUTURAL DA RESPOSTA OBRIGATÓRIA\n\n"
        "Para garantir clareza absoluta ao criador, sua resposta final deve seguir rigorosamente o seguinte padrão estrutural:\n\n"
        "1. **Veredicto Explícito:** Inicie informando de forma clara e destacada o status da auditoria (**APROVADO** ou **REPROVADO**).\n"
        "2. **Justificativa Detalhada por Critérios Multi-Ângulo:** Apresente os pilares avaliados comparando o vídeo com o conjunto de imagens oficiais enviadas.\n"
        "3. **Apontamento de Erros (Em caso de reprovação):** Descreva minuciosamente o erro encontrado (ex: 'A alça do produto no vídeo difere estruturalmente da foto oficial...'), citando o impacto regulatório na plataforma.\n"
        "4. **Tom Profissional e Orientativo:** Mantenha um tom prestativo, técnico, analítico e focado em proteger a Classificação de Integridade do Criador contra punições, quedas de alcance e devoluções."
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
    
    # Upload de arquivos (Suporte a até 4 imagens e vídeo)
    col1, col2 = st.columns(2)
    with col1:
        uploaded_images = st.file_uploader("Envie as imagens oficiais da vitrine (Até 4 imagens para análise multi-ângulo):", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    with col2:
        uploaded_video = st.file_uploader("Envie o vídeo do criador para auditoria:", type=["mp4", "mov", "avi"])

    if st.button("🚀 Iniciar Auditoria Multi-Ângulo Rigorosa"):
        if uploaded_video and uploaded_images:
            with st.spinner("Realizando análise cruzada multi-ângulo e micro-verificação geométrica..."):
                model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=SYSTEM_PROMPT_DI_CHECK)
                
                content_parts = []
                
                # Adiciona as imagens de referência (limitadas a 4)
                for img in uploaded_images[:4]:
                    content_parts.append({"mime_type": img.type, "data": img.getvalue()})
                
                # Adiciona o vídeo
                content_parts.append({"mime_type": uploaded_video.type, "data": uploaded_video.getvalue()})
                
                content_parts.append("Realize a auditoria multi-ângulo completa deste vídeo confrontando-o com o conjunto de imagens oficiais enviadas, aplicando rigor total a micro-detalhes, alças, puxadores, tampas e diretrizes do TikTok Shop.")
                
                response = model.generate_content(content_parts)
                
                st.markdown("### Resultado da Auditoria DI CHECK:")
                st.markdown(response.text)
        else:
            st.warning("Por favor, envie ao menos uma imagem de referência e o vídeo para iniciar a análise.")
else:
    st.info("Insira sua chave de API do Gemini acima para habilitar o painel de auditoria.")
