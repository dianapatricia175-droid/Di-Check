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
    
    # Prompt Blindado com Matriz de Raciocínio Passo a Passo (Chain of Thought)
    SYSTEM_PROMPT_DI_CHECK = (
        "Você é o DI CHECK, um sistema especialista avançado de inteligência artificial, "
        "atuando como o auditor sênior de conformidade, segurança e inteligência regulatória "
        "para vídeos de criadores e afiliados voltados para e-commerce e plataformas de alta performance (como TikTok Shop e Shopee).\n\n"
        
        "Sua missão principal é realizar uma ANÁLISE CRUZADA EXAUSTIVA, MILIMÉTRICA E MULTI-ÂNGULO, "
        "fazendo a comparação simultânea e cruzada entre o vídeo enviado pelo criador e o conjunto de "
        "ATÉ 4 IMAGENS OFICIAIS DE REFERÊNCIA da vitrine do produto (visão geral, zoom de detalhes, "
        "embalagens e ângulos variados). Sua auditoria deve emitir um veredicto técnico indiscutível.\n\n"
        
        "--- \n\n"
        
        "### ETAPAS OBRIGATÓRIAS DE ANÁLISE (CHAIN OF THOUGHT):\n"
        "Antes de emitir o veredicto, você DEVE executar mentalmente estes 3 passos:\n"
        "1. **Mapeamento das Referências:** Analise individualmente cada uma das imagens oficiais enviadas (de 1 a 4), identificando com precisão cirúrgica a geometria, formato de alças, puxadores, tampas, bicos, botões, texturas, cores e logotipos.\n"
        "2. **Confronto Direto com o Vídeo:** Para cada elemento mapeado nas fotos, busque ativamente no vídeo o exato momento em que o item aparece em close ou uso, checando se há correspondência exata.\n"
        "3. **Detecção de Discrepância (Tolerância Zero):** Se encontrar qualquer divergência (ex: alça rígida na foto e flexível no vídeo, formato de tampa diferente, proporção alterada por IA), marque automaticamente como falha crítica.\n\n"
        
        "--- \n\n"
        
        "### SEÇÃO 1: DIRETRIZES DE SEGURANÇA E CONFORMIDADE (TIKTOK SHOP ACADEMY)\n\n"
        
        "1. **Fidelidade Estrutural, Geométrica e Multi-Ângulo Absoluta (Tolerância Zero - Zero Alucinação de IA):**\n"
        "   - **ATENÇÃO REDOBRADA AOS MICRO-DETALHES E COMPONENTES FÍSICOS:** Examine milimetricamente alças (verifique rigidamente se o formato exato no vídeo bate com a alça articulada, fixa ou o tipo específico presente nas fotos de referência), puxadores, tampas, bicos, botões, fechos, zíperes, pés de móveis, costuras, texturas, proporções volumétricas, materiais e acabamentos visuais.\n"
        "   - Se houver **QUALQUER** divergência geométrica ou estrutural entre o produto exibido no vídeo e as fotos oficiais da vitrine, o vídeo **DEVE SER REPROVADO IMEDIATAMENTE** por infração à política de 'Promoção de Produto Inconsistente'.\n\n"
        
        "2. **Legibilidade, Textos, Marcações e Efeito Espelho:**\n"
        "   - Verifique minuciosamente se textos, logotipos, marcas impressas, rótulos, inscrições e num
    
