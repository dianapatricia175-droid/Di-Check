import streamlit as st
from google import genai
import os
import time

# Configuração da página do aplicativo com layout moderno (Wide)
st.set_page_config(
    page_title="DI CHECK - Auditoria Multi-Ângulo (Foto vs. Vídeo)",
    page_icon="🛡️",
    layout="wide"
)

# Estilização CSS personalizada para o painel corporativo
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
    </style>
""", unsafe_allow_html=True)

# Sidebar corporativa informativa
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/security-checked.png", width=70)
    st.markdown("### 🛡️ DI CHECK System")
    st.info("Painel de auditoria avançada com suporte a múltiplos ângulos de referência (Foto 1 obrigatória + até 3 opcionais).")
    st.markdown("---")
    st.markdown("**Critérios de Alta Precisão:**")
    st.markdown("✔️ Controlo de Inconsistências (Alucinações de IA)")
    st.markdown("✔️ Comparação Multi-Ângulo (Frente, Verso, Lados)")
    st.markdown("✔️ Controlo de Resolução, Borrões e Espelho")
    st.markdown("---")
    st.caption("Versão 4.0.0 - Multi-Angle AI Audit")

# Cabeçalho Principal
st.markdown('<p class="main-header">🛡️ DI CHECK - Auditoria Multi-Ângulo</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Insira a foto principal de referência e ângulos opcionais para cruzamento total com o vídeo gerado.</p>', unsafe_allow_html=True)

st.divider()

# Configuração da Chave da API
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 **Chave da API do Gemini não encontrada!** Adicione a chave nos *Secrets* do Streamlit Cloud.")
else:
    client = genai.Client(api_key=api_key)

    # Layout em colunas: Esquerda (Imagens de Referência) | Direita (Vídeo e Botão)
    col_esq, col_dir = st.columns([1, 1], gap="large")

    with col_esq:
        st.markdown("### 🖼️ 1. Imagens de Referência da Loja")
        st.caption("Adicione até 4 imagens para validação estrutural completa.")
        
        img1 = st.file_uploader("📸 Imagem 1: Frente / Principal (Obrigatória)", type=["jpg", "jpeg", "png"], key="img1")
        img2 = st.file_uploader("📐 Imagem 2: Verso ou Ângulo Alternativo (Opcional)", type=["jpg", "jpeg", "png"], key="img2")
        img3 = st.file_uploader("🔍 Imagem 3: Detalhes / Acabamento (Opcional)", type=["jpg", "jpeg", "png"], key="img3")
        img4 = st.file_uploader("🔄 Imagem 4: Outro Ângulo / Etiqueta (Opcional)", type=["jpg", "jpeg", "png"], key="img4")

    with col_dir:
        st.markdown("### 🎬 2. Vídeo Gerado para Auditoria")
        video_carregado = st.file_uploader(
            "Selecione o ficheiro de vídeo (.mp4, .mov, .avi)", 
            type=["mp4", "mov", "avi", "mkv"]
        )
        if video_carregado is not None:
            st.video(video_carregado)

    # Validação para habilitar o botão: Imagem 1 e Vídeo são estritamente obrigatórios
    if img1 is not None and video_carregado is not None:
        st.divider()
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            executar_auditoria = st.button("🚀 Executar Auditoria Multi-Ângulo", type="primary", use_container_width=True)

        if executar_auditoria:
            status_box = st.status("🔍 A preparar ficheiros e imagens para análise...", expanded=True)
            
            try:
                # Lista para acumular todos os recursos que serão enviados ao Gemini
                contents_to_send = []
                temp_files_to_clean = []

                # Processar Imagem 1 (Obrigatória)
                status_box.update(label="A processar Imagem 1 (Principal)...", state="running")
                with open("temp_img1.jpg", "wb") as f:
                    f.write(img1.getbuffer())
                f_obj1 = client.files.upload(file="temp_img1.jpg")
                contents_to_send.append(f_obj1)
                temp_files_to_clean.append("temp_img1.jpg")

                # Processar Imagens Opcionais (2, 3 e 4) dinamicamente se existirem
                imagens_opcionais = [img2, img3, img4]
                for idx, img_opc in enumerate(imagens_opcionais, start=2):
                    if img_opc is not None:
                        status_box.update(label=f"A processar Imagem {idx} (Ângulo alternativo)...", state="running")
                        fname = f"temp_img{idx}.jpg"
                        with open(fname, "wb") as f:
                            f.write(img_opc.getbuffer())
                        f_obj = client.files.upload(file=fname)
                        contents_to_send.append(f_obj)
                        temp_files_to_clean.append(fname)

                # Processar Vídeo
                status_box.update(label="A guardar e enviar o vídeo...", state="running")
                with open("temp_video.mp4", "wb") as f:
                    f.write(video_carregado.getbuffer())
                video_file = client.files.upload(file="temp_video.mp4")
                temp_files_to_clean.append("temp_video.mp4")
                
                status_box.update(label="A aguardar processamento dos multimédia na nuvem da Google...", state="running")
                while video_file.state.name == "PROCESSING":
                    time.sleep(3)
                    video_file = client.files.get(name=video_file.name)
                    if video_file.state.name == "FAILED":
                        raise Exception("O processamento do vídeo falhou nos servidores.")

                # Adicionar o vídeo à lista de conteúdos enviados
                contents_to_send.append(video_file)

                status_box.update(label="A executar cruzamento rigoroso multi-ângulo...", state="running")

                # Prompt especializado considerando as múltiplas imagens e o vídeo
                prompt_auditoria = (
                    "Você é um auditor sênior de conformidade, qualidade visual e prevenção de inconsistências para o TikTok Shop e Shopee. "
                    "Analise com rigor absoluto e implacável o conjunto de **Imagens de Referência da Loja fornecidas (de 1 até 4 ângulos)** em comparação estrita com o **Vídeo enviado**. "
                    "O seu foco principal é detetar **inconsistências de produto e alucinações de inteligência artificial** (como botões extras, laços, fechos alterados, proporções divergentes ou elementos estruturais que aparecem no vídeo mas NÃO correspondem às referências visuais oficiais). "
                    "\n\n"
                    "Gere obrigatoriamente uma **Checklist de Inspeção Detalhada** avaliando:\n"
                    "1. **Consistência Estrutural (Fotos vs. Vídeo):** O produto exibido no vídeo mantém fidelidade absoluta às imagens de referência fornecidas (considerando frente, verso e detalhes)? Atribua ❌ se houver discrepâncias físicas geradas por IA.\n"
                    "2. **Autenticidade de Marcas e Rótulos:** Verifique se os logótipos e textos estão corretos e legítimos.\n"
                    "3. **Qualidade Técnica do Vídeo:** O vídeo tem boa resolução? Os textos estão nítidos e legíveis? Atribua ❌ se houver borrões graves ou **palavras invertidas/espelhadas**.\n"
                    "4. **Variações de Cores:** Variações de cores legítimas do mesmo produto são permitidas desde que a geometria e o modelo sejam idênticos às fotos de referência.\n"
                    "\n"
                    "REGRAS RÍGIDAS:\n"
                    "- Se houver **qualquer inconsistência de produto** ou erro técnico grave, o veredicto final DEVE ser obrigatoriamente **[REPROVADO]**.\n"
                    "- O veredicto **[APROVADO]** só será emitido se todos os critérios estiverem rigorosamente alinhados com as imagens de referência."
                )

                contents_to_send.append(prompt_auditoria)

                # Chamada com retentativas inteligentes para o erro 503
                sucesso = False
                response = None
                ultimo_erro = None

                for tentativa in range(5):
                    try:
                        response = client.models.generate_content(
                            model='gemini-3.8-flash',
                            contents=contents_to_send
                        )
                        if response and hasattr(response, 'text') and response.text:
                            sucesso = True
                            break
                    except Exception as err:
                        ultimo_erro = err
                        time.sleep(8)

                if sucesso and response and response.text:
                    status_box.update(label="Auditoria concluída com sucesso!", state="complete", expanded=False)
                    
                    st.markdown("### 📋 Relatório Executivo Multi-Ângulo")
                    
                    texto_resposta = response.text
                    
                    if "[REPROVADO]" in texto_resposta.upper() or "❌" in texto_resposta:
                        st.error("🚨 **VEREDICTO CORPORATIVO: REPROVADO (INCONSISTÊNCIA DETETADA / NÃO PUBLIQUE)**")
                    else:
                        st.success("✅ **VEREDICTO CORPORATIVO: APROVADO (FIEL ÀS FOTOS DE REFERÊNCIA)**")
                        
                    st.markdown("---")
                    st.write(texto_resposta)
                else:
                    status_box.update(label="Falha na resposta da IA", state="error")
                    st.error(f"Os servidores estão com alta procura no momento (Erro 503). Detalhe técnico: {ultimo_erro}")

                # Limpar ficheiros temporários locais
                for f_temp in temp_files_to_clean:
                    if os.path.exists(f_temp):
                        os.remove(f_temp)

            except Exception as e:
                status_box.update(label="Erro crítico no processo", state="error")
                st.error(f"Ocorreu um erro durante o processamento: {e}")
                for f_temp in temp_files_to_clean:
                    if os.path.exists(f_temp):
                        os.remove(f_temp)
    else:
        st.info("ℹ️ Para iniciar a auditoria, carregue obrigatoriamente a **Imagem 1 (Principal)** e o **Vídeo** nos campos indicados.")
