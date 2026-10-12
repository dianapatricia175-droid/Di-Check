import streamlit as st
from google import genai
import os
import time

# Configuração da página do aplicativo com layout moderno
st.set_page_config(
    page_title="DI CHECK - Auditoria Inteligente",
    page_icon="🛡️",
    layout="wide" # Alterado para wide para dar um aspeto de painel corporativo (Dashboard)
)

# Estilização CSS personalizada para dar aspeto de Painel de Auditoria de Alta Tecnologia
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar corporativa informativa
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/security-checked.png", width=70)
    st.markdown("### 🛡️ DI CHECK System")
    st.info("Painel autónomo de validação e conformidade visual integrado com a inteligência artificial Gemini para o TikTok Shop e Shopee.")
    st.markdown("---")
    st.markdown("**Critérios Ativos de Inspeção:**")
    st.markdown("✔️ Autenticidade de Marcas/Logotipos")
    st.markdown("✔️ Controlo de Resolução e Borrões")
    st.markdown("✔️ Validação de Textos Invertidos/Espelho")
    st.markdown("✔️ Exceção Segura para Variações de Cores")
    st.markdown("---")
    st.caption("Versão 3.8.2 - Enterprise Grade")

# Cabeçalho Principal
st.markdown('<p class="main-header">🛡️ DI CHECK - Auditoria de Vídeo Inteligente</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Plataforma de alta precisão para validação pré-publicação no TikTok Shop e Shopee.</p>', unsafe_allow_html=True)

st.divider()

# Configuração da Chave da API
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 **Chave da API do Gemini não encontrada!** Adicione a chave nos *Secrets* do Streamlit Cloud.")
else:
    client = genai.Client(api_key=api_key)

    # Layout em colunas para a área de upload e pré-visualização
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### 📥 1. Envio de Ficheiro")
        video_carregado = st.file_uploader(
            "Selecione o ficheiro de vídeo (.mp4, .mov, .avi)", 
            type=["mp4", "mov", "avi", "mkv"]
        )
        
        if video_carregado is not None:
            st.success("Ficheiro validado e pronto para análise.")

    with col2:
        st.markdown("### 🎬 2. Pré-visualização do Conteúdo")
        if video_carregado is not None:
            st.video(video_carregado)
        else:
            st.markdown("""
                <div class="metric-card">
                    <b>Aguardando ficheiro...</b><br>
                    Faça o upload de um vídeo ao lado para ativar o motor de inspeção visual detalhada.
                </div>
            """, unsafe_allow_html=True)

    if video_carregado is not None:
        st.divider()
        
        # Secção centralizada para o botão de execução
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            executar_auditoria = st.button("🚀 Executar Auditoria de Precisão", type="primary", use_container_width=True)

        if executar_auditoria:
            status_box = st.status("🔍 A iniciar motor de auditoria...", expanded=True)
            
            try:
                status_box.update(label="A preparar o ficheiro temporário...", state="running")
                with open("temp_video.mp4", "wb") as f:
                    f.write(video_carregado.getbuffer())

                status_box.update(label="A transmitir o vídeo para o ambiente seguro da Google...", state="running")
                video_file = client.files.upload(file="temp_video.mp4")
                
                status_box.update(label="A aguardar processamento e renderização dos fotogramas...", state="running")
                while video_file.state.name == "PROCESSING":
                    time.sleep(3)
                    video_file = client.files.get(name=video_file.name)
                    if video_file.state.name == "FAILED":
                        raise Exception("O processamento do vídeo falhou nos servidores da Google.")

                status_box.update(label="A executar varredura quântica de conformidade com IA...", state="running")

                # Prompt definitivo ultra-rigoroso cobrindo todas as regras estabelecidas
                prompt_auditoria = (
                    "Você é um auditor sênior de conformidade, qualidade visual e segurança de contas para o TikTok Shop e Shopee. "
                    "Analise este vídeo quadro a quadro com rigor absoluto, implacável e sem margem para erros. "
                    "Você deve gerar obrigatoriamente uma **Checklist de Inspeção Detalhada**, avaliando os seguintes pontos com os símbolos corretos: "
                    "- Use **✅** apenas se o item estiver perfeito, em alta definição e total conformidade. "
                    "- Use **❌** se encontrar qualquer anomalia real, logotipos falsificados de terceiros, **baixa resolução (ex: abaixo de 720p), letras miúdas borradas, distorcidas, ilegíveis OU SE HOUVER PALAVRAS AO CONTRÁRIO (invertidas, espelhadas ou ilegíveis)** nas embalagens e rótulos. "
                    "\n\n"
                    "Itens obrigatórios da Checklist a avaliar:\n"
                    "1. **Autenticidade de Logotipos e Marcas:** Verifique se existem marcas concorrentes ou logotipos de terceiros não autorizados. Nota importante: Exiba ✅ se o logotipo apresentado pertencer legitimamente ao produto anunciado (marcas próprias ou oficiais do lojista), sem falsos positivos.\n"
                    "2. **Resolução, Nitidez, Orientação e Legibilidade de Textos:** O vídeo tem resolução adequada? Os textos descritivos e especificações impressas estão nítidos? **Atenção redobrada:** Se as palavras estiverem invertidas/ao contrário (efeito espelho incorreto), borradas, cortadas ou com baixa resolução que dificulte a leitura, **este item deve receber obrigatoriamente ❌**.\n"
                    "3. **Variações de Cores, Modelos e Linhas de Produtos:** Avalie se há múltiplas versões, cores ou potes exibidos no vídeo. **REGRA DE OURO:** A apresentação de variações de cores, sabores ou modelos lado a lado é uma prática comercial legítima e ESPERADA no e-commerce. Nunca considere variações de cores/modelos como erro ou inconsistência estrutural (atribua ✅).\n"
                    "4. **Riscos de Moderação (Robôs da Plataforma):** Inspecionando elementos que possam gerar penalização real pelas regras do marketplace.\n"
                    "\n"
                    "REGRAS RÍGIDAS DE AVALIAÇÃO:\n"
                    "- Se houver **pelo menos um** erro real marcado com ❌ (incluindo baixa resolução, texto ilegível ou palavras ao contrário/invertidas), o veredicto final DEVE ser obrigatoriamente **[REPROVADO]** com a explicação detalhada do motivo.\n"
                    "- O vídeo só poderá receber o veredicto **[APROVADO]** se e somente se todos os itens essenciais estiverem marcados com ✅."
                )

                # Chamada com retentativas inteligentes (até 5 tentativas e 8 segundos de pausa para contornar o erro 503)
                sucesso = False
                response = None
                ultimo_erro = None

                for tentativa in range(5):
                    try:
                        response = client.models.generate_content(
                            model='gemini-3.8-flash',
                            contents=[video_file, prompt_auditoria]
                        )
                        if response and hasattr(response, 'text') and response.text:
                            sucesso = True
                            break
                    except Exception as err:
                        ultimo_erro = err
                        time.sleep(8)

                if sucesso and response and response.text:
                    status_box.update(label="Auditoria concluída com sucesso!", state="complete", expanded=False)
                    
                    st.markdown("### 📋 Relatório Executivo de Auditoria")
                    
                    texto_resposta = response.text
                    
                    # Caixa de destaque visual para o resultado final
                    if "[REPROVADO]" in texto_resposta.upper() or "❌" in texto_resposta:
                        st.error("🚨 **VEREDICTO CORPORATIVO: REPROVADO (RISCO DE PENALIZAÇÃO / NÃO PUBLIQUE)**")
                    else:
                        st.success("✅ **VEREDICTO CORPORATIVO: APROVADO PARA PUBLICAÇÃO IMEDIATA**")
                        
                    st.markdown("---")
                    st.write(texto_resposta)
                else:
                    status_box.update(label="Falha na resposta da IA", state="error")
                    st.error(f"Os servidores estão com alta procura no momento (Erro 503). Detalhe técnico: {ultimo_erro}")

                if os.path.exists("temp_video.mp4"):
                    os.remove("temp_video.mp4")

            except Exception as e:
                status_box.update(label="Erro crítico no processo", state="error")
                st.error(f"Ocorreu um erro durante o processamento: {e}")
                if os.path.exists("temp_video.mp4"):
                    os.remove("temp_video.mp4")
