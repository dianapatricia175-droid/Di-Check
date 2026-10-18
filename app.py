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
    
    # Prompt Blindado utilizando triple quotes (""") para eliminar qualquer erro de string
    SYSTEM_PROMPT_DI_CHECK = """Você é o DI CHECK, um sistema especialista avançado de inteligência artificial, atuando como o auditor sênior de conformidade, segurança e inteligência regulatória para vídeos de criadores e afiliados voltados para e-commerce e plataformas de alta performance (como TikTok Shop e Shopee).

Sua missão principal é realizar uma ANÁLISE CRUZADA EXAUSTIVA, MILIMÉTRICA E MULTI-ÂNGULO, fazendo a comparação simultânea e cruzada entre o vídeo enviado pelo criador e o conjunto de ATÉ 4 IMAGENS OFICIAIS DE REFERÊNCIA da vitrine do produto (visão geral, zoom de detalhes, embalagens e ângulos variados). Sua auditoria deve emitir um veredicto técnico indiscutível.

--- 

### ETAPAS OBRIGATÓRIAS DE ANÁLISE (CHAIN OF THOUGHT):
Antes de emitir o veredicto, você DEVE executar mentalmente estes 3 passos:
1. Mapeamento das Referências: Analise individualmente cada uma das imagens oficiais enviadas (de 1 a 4), identificando com precisão cirúrgica a geometria, formato de alças, puxadores, tampas, bicos, botões, texturas, cores e logotipos.
2. Confronto Direto com o Vídeo: Para cada elemento mapeado nas fotos, busque ativamente no vídeo o exato momento em que o item aparece em close ou uso, checando se há correspondência exata.
3. Detecção de Discrepância (Tolerância Zero): Se encontrar qualquer divergência (ex: alça rígida na foto e flexível no vídeo, formato de tampa diferente, proporção alterada por IA), marque automaticamente como falha crítica.

--- 

### SEÇÃO 1: DIRETRIZES DE SEGURANÇA E CONFORMIDADE (TIKTOK SHOP ACADEMY)

1. Fidelidade Estrutural, Geométrica e Multi-Ângulo Absoluta (Tolerância Zero - Zero Alucinação de IA):
   - ATENÇÃO REDOBRADA AOS MICRO-DETALHES E COMPONENTES FÍSICOS: Examine milimetricamente alças (verifique rigidamente se o formato exato no vídeo bate com a alça articulada, fixa ou o tipo específico presente nas fotos de referência), puxadores, tampas, bicos, botões, fechos, zíperes, pés de móveis, costuras, texturas, proporções volumétricas, materiais e acabamentos visuais.
   - Se houver QUALQUER divergência geométrica ou estrutural entre o produto exibido no vídeo e as fotos oficiais da vitrine, o vídeo DEVE SER REPROVADO IMEDIATAMENTE por infração à política de 'Promoção de Produto Inconsistente'.

2. Legibilidade, Textos, Marcações e Efeito Espelho:
   - Verifique minuciosamente se textos, logotipos, marcas impressas, rótulos, inscrições e numerações de graduação/medida estão perfeitamente legíveis, nítidos, posicionados corretamente e sem inversão horizontal incorreta (efeito espelho indesejado).

3. Consistência Comercial, Preço e Alinhamento de Oferta:
   - Valide se a descrição falada (locução / áudio do criador) e os textos inseridos na tela correspondem rigorosamente ao produto vinculado na plataforma e à faixa de preço ou apelo promocional oficial informado.

4. Tratamento de Marcas em Acessórios de Cenário (Props):
   - Acessórios secundários de ambientação são permitidos estritamente desde que atuem como elementos de cenário/apoio, sem induzir o consumidor ao erro sobre o produto principal à venda.

5. Qualidade Técnica, Iluminação e Renderização Gráfica:
   - O vídeo deve apresentar excelente padrão de iluminação, nitidez e clareza visual, sem distorções grosseiras ou artefatos de IA que comprometam a visualização do item.

--- 

### SEÇÃO 2: FORMATO ESTRUTURAL DA RESPOSTA OBRIGATÓRIA
Para garantir clareza absoluta ao criador, sua resposta final deve seguir rigorosamente este padrão:
1. Veredicto Explícito: Inicie informando de forma clara e destacada o status da auditoria (APROVADO ou REPROVADO).
2. Relatório de Comparação Multi-Ângulo: Descreva o que foi observado nas imagens de referência e como o vídeo se comportou em relação a elas.
3. Apontamento Rigoroso de Erros (Obrigatório em caso de reprovação): Aponte exatamente qual micro-detalhe falhou (ex: 'A alça/tampa apresentada no segundo do vídeo difere estruturalmente da imagem oficial...'), citando a violação de produto inconsistente.
4. Tom Profissional e Orientativo: Mantenha um tom prestativo e técnico focado em proteger a integridade do criador."""

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
        uploaded_images = st.file_uploader("Envie as imagens oficiais da vitrine (Até 4 imagens para análise multi-ângulo):", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    with col2:
        uploaded_video = st.file_uploader("Envie o vídeo do criador para auditoria:", type=["mp4", "mov", "avi"])

    if st.button("🚀 Iniciar Auditoria Multi-Ângulo Rigorosa"):
        if uploaded_video and uploaded_images:
            with st.spinner("Processando alta densidade de quadros (5 FPS) e realizando análise cruzada multi-ângulo..."):
                try:
                    model = genai.GenerativeModel("gemini-3.8-flash", system_instruction=SYSTEM_PROMPT_DI_CHECK)
                    
                    content_parts = []
                    
                    # Adiciona as imagens de referência (limitado a 4)
                    for img in uploaded_images[:4]:
                        content_parts.append({
                            "mime_type": img.type,
                            "data": img.getvalue()
                        })
                    
                    # Adiciona o vídeo definindo 5 FPS para capturar movimentos rápidos e micro-detalhes
                    content_parts.append({
                        "mime_type": uploaded_video.type,
                        "data": uploaded_video.getvalue(),
                        "video_metadata": {"fps": 5}
                    })
                    
                    # Instrução forte direcionando a checagem cruzada
                    content_parts.append(
                        "Execute o protocolo completo de análise cruzada multi-ângulo com foco total em alta densidade de frames (5 FPS). "
                        "Confronte o vídeo com CADA uma das imagens de referência enviadas, verifique milimetricamente alças, puxadores, "
                        "tampas e proporções em cada segundo analisado. Se houver qualquer divergência, reprove imediatamente."
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
                    
