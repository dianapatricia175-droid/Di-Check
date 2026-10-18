import streamlit as st
from google import genai
from google.genai import types
import cv2
import time
import tempfile
import os
import math

# ============================================================
# DI CHECK — Auditoria visual de produtos para TikTok Shop/Shopee
# ============================================================

st.set_page_config(
    page_title="DI CHECK - Auditoria TikTok/Shopee",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
.main { background-color: #0f172a; color: #f8fafc; }
.stTextInput input {
    background-color: #1e293b; color: #ffffff;
    border-radius: 8px; border: 1px solid #334155;
}
.stFileUploader {
    background-color: #1e293b; border: 2px dashed #475569;
    border-radius: 12px; padding: 15px;
}
.stButton button {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    color: white; font-weight: bold; border-radius: 8px;
    padding: 0.6rem 1.2rem; border: none;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    width: 100%;
}
.stButton button:hover {
    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.5);
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align:center;color:#38bdf8;'>🛡️ DI CHECK — Sistema de Auditoria Rigorosa</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;color:#94a3b8;font-size:1.05rem;'>"
    "Auditoria visual assistida para TikTok Shop e Shopee: fidelidade do produto, "
    "componentes, textos, elementos gráficos e evidências por timestamp.</p>",
    unsafe_allow_html=True
)

# Não registre nem armazene a chave da API. Para uso em produção,
# prefira st.secrets ou variável de ambiente.
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    api_key = st.text_input(
        "🔑 Insira sua Gemini API Key:",
        type="password",
        placeholder="Cole sua chave aqui..."
    )

SYSTEM_PROMPT_DI_CHECK = """
Você é o DI CHECK, um assistente de auditoria visual rigorosa para vídeos
de produtos destinados ao TikTok Shop e à Shopee.

OBJETIVO
Comparar as imagens oficiais de referência com os quadros do vídeo que
foram efetivamente fornecidos. Identifique evidências visíveis, sem
inventar detalhes e sem afirmar que analisou quadros que não recebeu.

CRITÉRIOS DE AUDITORIA

1. FIDELIDADE DO PRODUTO
- Compare categoria, modelo, formato, cor, proporções relativas,
  acabamento, textura, quantidade de peças e acessórios visíveis.
- Confira separadamente tampa, alça, bico, puxadores, botões,
  encaixes, conectores, costuras, fechos, base e demais componentes
  relevantes ao tipo de produto.
- Compare vários ângulos quando estiverem disponíveis.
- Considere as variações de cor/modelo que estiverem claramente
  contempladas nas imagens oficiais. Não reprove só por uma cor
  diferente se ela for uma variação apresentada na referência.
- Não conclua que dois componentes são iguais se o ângulo, a resolução,
  o foco ou a oclusão não permitirem verificar.

2. ELEMENTOS GRÁFICOS TEMPORÁRIOS
- Detecte textos sobrepostos, setas, emojis, stickers, desenhos,
  efeitos, molduras, marcas d'água, @s, nomes de perfis e logotipos.
- Registre quando aparecem e desaparecem, usando os timestamps fornecidos.
- Diferencie elementos gráficos sobrepostos de componentes físicos.
- A presença de um elemento gráfico, por si só, não prova violação:
  descreva-o e indique que a conformidade com a plataforma deve ser
  avaliada conforme a política aplicável.
- Não declare que um vídeo foi roubado nem que há violação de direitos
  autorais sem evidências suficientes.

3. MARCAS E PROPRIEDADE INTELECTUAL
- Registre marcas e logotipos legíveis e possíveis imitações visuais.
- Não declare falsificação apenas por semelhança visual ou por falta
  de informação. Marque suspeitas como suspeitas.
- Não invente uma marca quando o texto estiver ilegível.

4. TEXTOS E EMBALAGEM
- Verifique legibilidade, orientação, possíveis inversões espelhadas,
  discrepâncias de rótulo e incompatibilidades visíveis.
- Não classifique um texto como incorreto se estiver ilegível.

5. CONSISTÊNCIA COMERCIAL
- Compare afirmações audíveis/visíveis com as informações fornecidas
  pelo usuário, se houver. Não presuma preço, material, capacidade,
  desempenho ou características que não tenham sido fornecidos.
- A qualidade visual não é, isoladamente, prova de violação.

6. DISCIPLINA DE EVIDÊNCIAS
- Para cada achado, indique timestamp, quadro/índice quando disponível,
  o que é visto, comparação com referência e nível de certeza.
- Use: CONFIRMADO, SUSPEITA ou NÃO VERIFICÁVEL.
- Uma divergência concreta e relevante deve ser destacada.
- Se um critério crítico não puder ser verificado, não recomende aprovação
  automática; use INCONCLUSIVO — REVISÃO NECESSÁRIA.
- Não diga “análise de 100% dos quadros” a menos que todos os quadros
  originais tenham sido realmente processados.
- Não alegue que o vídeo está em conformidade com todas as regras atuais
  das plataformas sem uma verificação independente das políticas oficiais.

Formato do relatório de cada lote:
LOTE [número]
Para cada quadro:
- Timestamp e índice:
- Produto/características observadas:
- Comparação com as referências:
- Divergências confirmadas:
- Suspeitas:
- Elementos gráficos temporários:
- Itens não verificáveis:

Ao final, liste timestamps que precisam de revisão.
Não emita aprovação ou reprovação final nesta etapa.
"""

PROMPT_CONSOLIDACAO = """
Você é o auditor final do DI CHECK. Consolide todos os relatórios dos
lotes sem descartar evidências individuais.

Escolha exatamente um veredicto:
🔴 REPROVADO — há uma divergência visual confirmada e relevante, ou
um risco concreto que exige interromper a publicação até esclarecimento.
🟡 INCONCLUSIVO — REVISÃO NECESSÁRIA — faltam imagens, ângulos,
referências ou evidências para uma decisão segura.
🟢 SEM DIVERGÊNCIAS VISUAIS DETECTADAS — nenhum problema visual foi
detectado nos elementos efetivamente analisados. Isso não garante
ausência absoluta de infrações nem aprovação pela plataforma.

Regras:
- Não confunda suspeita com infração confirmada.
- Não declare falsificação apenas por semelhança visual.
- Não reprove por diferença de cor se essa variação estiver contemplada
  nas referências oficiais.
- Não ignore uma divergência só porque aparece em um único quadro.
- Cite timestamps, índices e evidências concretas.
- Separe a análise visual da conformidade jurídica/política.
- Se um item crítico estiver oculto, desfocado ou sem referência adequada,
  o resultado não pode ser “sem divergências visuais detectadas”.
- Não afirme precisão de 100%.
- Explique que as regras das plataformas devem ser conferidas nas fontes
  oficiais atualizadas.

Formato:
1. VEREDICTO
2. RESUMO EXECUTIVO
3. PAINEL DE CRITÉRIOS, cada um com:
   CONFORME VISUALMENTE / DIVERGÊNCIA CONFIRMADA /
   SUSPEITA / NÃO VERIFICÁVEL
4. DIVERGÊNCIAS COM TIMESTAMP E EVIDÊNCIA
5. ELEMENTOS GRÁFICOS TEMPORÁRIOS
6. LIMITAÇÕES E PONTOS NÃO VERIFICÁVEIS
7. RECOMENDAÇÃO ANTES DA PUBLICAÇÃO
"""

def extrair_quadros(video_path, amostragem_fps=4, largura_max=1280):
    """Extrai quadros em intervalos regulares e registra timestamp/índice."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Não foi possível abrir o vídeo enviado.")

    fps_original = cap.get(cv2.CAP_PROP_FPS)
    total_quadros = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if not fps_original or fps_original <= 0 or total_quadros <= 0:
        cap.release()
        raise ValueError("Não foi possível identificar FPS ou quantidade de quadros.")

    duracao = total_quadros / fps_original
    intervalo = max(1, round(fps_original / amostragem_fps))
    quadros = []
    indice = 0

    while True:
        sucesso, frame = cap.read()
        if not sucesso:
            break

        if indice % intervalo == 0:
            altura, largura = frame.shape[:2]
            if largura > largura_max:
                nova_altura = max(1, round(altura * largura_max / largura))
                frame = cv2.resize(
                    frame, (largura_max, nova_altura),
                    interpolation=cv2.INTER_AREA
                )

            ok, buffer = cv2.imencode(
                ".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 95]
            )
            if ok:
                quadros.append({
                    "timestamp": indice / fps_original,
                    "indice": indice,
                    "bytes": buffer.tobytes()
                })
        indice += 1

    cap.release()
    if not quadros:
        raise ValueError("Nenhum quadro pôde ser extraído do vídeo.")

    return quadros, duracao, fps_original, total_quadros


def formatar_timestamp(segundos):
    minutos = int(segundos // 60)
    segundos_restantes = segundos - minutos * 60
    return f"{minutos:02d}:{segundos_restantes:05.2f}"


def auditar_lote(client, modelo, imagens_referencia, quadros, numero_lote, total_lotes):
    prompt = (
        SYSTEM_PROMPT_DI_CHECK
        + f"\n\nAnalise o LOTE {numero_lote} DE {total_lotes}. "
        + "As imagens oficiais são apresentadas primeiro. Em seguida, "
        + "cada quadro do vídeo vem com timestamp e índice. "
        + "Compare cada quadro com as referências e siga o formato definido."
    )

    conteudos = [prompt]
    for i, imagem in enumerate(imagens_referencia, start=1):
        conteudos.append(f"IMAGEM OFICIAL DE REFERÊNCIA {i}")
        conteudos.append(
            types.Part.from_bytes(
                data=imagem.getvalue(),
                mime_type=imagem.type or "image/jpeg"
            )
        )

    for quadro in quadros:
        ts = formatar_timestamp(quadro["timestamp"])
        conteudos.append(
            f"QUADRO DO VÍDEO — timestamp {ts} — índice original {quadro['indice']}"
        )
        conteudos.append(
            types.Part.from_bytes(
                data=quadro["bytes"],
                mime_type="image/jpeg"
            )
        )

    resposta = client.models.generate_content(
        model=modelo,
        contents=conteudos,
        config=types.GenerateContentConfig()
    )
    texto = getattr(resposta, "text", None)
    if not texto:
        raise RuntimeError(f"O modelo não retornou texto no lote {numero_lote}.")
    return texto


# Interface de envio
st.markdown("---")
st.markdown("### 📁 Envio de arquivos para auditoria")

col_img, col_vid = st.columns(2)
with col_img:
    uploaded_images = st.file_uploader(
        "🖼️ Imagens oficiais da vitrine (até 4 fotos):",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )
with col_vid:
    uploaded_video = st.file_uploader(
        "🎥 Vídeo do criador para auditoria:",
        type=["mp4", "mov", "avi", "m4v"]
    )

col_a, col_b = st.columns(2)
with col_a:
    amostragem = st.select_slider(
        "Frequência da inspeção visual",
        options=[1, 2, 4, 8, 15],
        value=4,
        help="Mais quadros aumentam o tempo e o custo. Esta amostragem "
             "não equivale a inspecionar todos os quadros originais."
    )
with col_b:
    tamanho_lote = st.selectbox(
        "Quadros enviados por lote",
        options=[2, 4, 6, 8],
        index=2,
        help="Lotes menores podem facilitar a leitura de detalhes, "
             "mas aumentam o número de chamadas à API."
    )

modelo = st.text_input(
    "Modelo Gemini disponível na sua conta",
    value="gemini-3.8-flash",
    help="Confirme os modelos disponíveis na documentação/conta Google AI. "
         "Modelo padrão atualizado para gemini-3.8-flash conforme a mensagem de erro da sua conta. Se a API retornar outro erro, confira os modelos disponíveis no Google AI Studio."
)

st.caption(
    "Privacidade: o vídeo é processado temporariamente para a auditoria. "
    "A chave da API não é exibida. Confira os termos de retenção do provedor."
)

if st.button("🚀 Iniciar Auditoria Completa de Conformidade"):
    if not api_key:
        st.warning("Insira sua Gemini API Key.")
    elif not uploaded_images:
        st.warning("Envie pelo menos uma imagem oficial de referência.")
    elif len(uploaded_images) > 4:
        st.warning("Envie no máximo quatro imagens oficiais.")
    elif not uploaded_video:
        st.warning("Envie o vídeo que deseja auditar.")
    else:
        client = None
        video_path = None

        try:
            client = genai.Client(api_key=api_key)

            extensao = os.path.splitext(uploaded_video.name)[1].lower()
            if extensao not in [".mp4", ".mov", ".avi", ".m4v"]:
                extensao = ".mp4"

            with tempfile.NamedTemporaryFile(delete=False, suffix=extensao) as tmp:
                tmp.write(uploaded_video.getvalue())
                video_path = tmp.name

            with st.spinner("Extraindo quadros e registrando timestamps..."):
                quadros, duracao, fps_original, total_original = extrair_quadros(
                    video_path, amostragem_fps=amostragem
                )

            st.markdown("### 📹 Cobertura da inspeção")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Duração", f"{duracao:.2f} s")
            c2.metric("FPS original", f"{fps_original:.2f}")
            c3.metric("Quadros originais", f"{total_original}")
            c4.metric("Quadros inspecionados", f"{len(quadros)}")
            st.warning(
                "A inspeção usa amostragem. Ela não examina necessariamente todos os "
                "quadros originais e não garante 100% de detecção. Se a falha ocorrer "
                "em um instante muito curto, repita com frequência maior ou use "
                "inspeção de todos os quadros."
            )

            lotes = [
                quadros[i:i + tamanho_lote]
                for i in range(0, len(quadros), tamanho_lote)
            ]
            relatorios = []
            progresso = st.progress(0)
            status = st.empty()

            for numero, lote in enumerate(lotes, start=1):
                status.write(f"Analisando lote {numero} de {len(lotes)}...")
                relatorio = auditar_lote(
                    client=client,
                    modelo=modelo,
                    imagens_referencia=uploaded_images,
                    quadros=lote,
                    numero_lote=numero,
                    total_lotes=len(lotes)
                )
                relatorios.append(f"RELATÓRIO DO LOTE {numero}\n{relatorio}")
                progresso.progress(numero / len(lotes))

            status.write("Consolidando as evidências...")
            resposta_final = client.models.generate_content(
                model=modelo,
                contents=[
                    PROMPT_CONSOLIDACAO,
                    "\n\n".join(relatorios)
                ],
                config=types.GenerateContentConfig()
            )

            texto_final = getattr(resposta_final, "text", None)
            st.markdown("## 📊 Resultado da auditoria DI CHECK")
            if texto_final:
                st.markdown(texto_final)
            else:
                st.error(
                    "A consolidação não retornou um relatório válido. "
                    "Não considere o produto aprovado; revise os relatórios dos lotes."
                )

            with st.expander("Ver relatórios completos por lote"):
                for i, relatorio in enumerate(relatorios, start=1):
                    st.markdown(f"#### Lote {i}")
                    st.text(relatorio)

            # Disponibiliza os relatórios para guardar e revisar.
            texto_exportacao = (
                "DI CHECK — RELATÓRIO DE AUDITORIA\n\n"
                f"Duração: {duracao:.2f} s\n"
                f"FPS original: {fps_original:.2f}\n"
                f"Quadros originais: {total_original}\n"
                f"Quadros amostrados: {len(quadros)}\n"
                f"Frequência de amostragem: {amostragem} FPS\n\n"
                "VEREDICTO CONSOLIDADO\n"
                + (texto_final or "Não gerado")
                + "\n\nRELATÓRIOS POR LOTE\n\n"
                + "\n\n".join(relatorios)
            )
            st.download_button(
                "⬇️ Baixar relatório completo (.txt)",
                data=texto_exportacao,
                file_name="relatorio_di_check.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(
                f"Falha durante a auditoria: {e}\n\n"
                "Confira a chave, o nome do modelo, a conexão e os limites da API. "
                "Falha técnica não deve ser interpretada como aprovação. O erro anterior indicava que gemini-2.5-flash não estava disponível para sua conta; este arquivo agora usa gemini-3.8-flash por padrão."
            )
        finally:
            if video_path and os.path.exists(video_path):
                try:
                    os.unlink(video_path)
                except OSError:
                    pass
else:
    st.info(
        "💡 Insira sua chave Gemini, envie as imagens oficiais e o vídeo "
        "para iniciar a auditoria."
        )
            
