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
Você é o DI CHECK, um auditor VISUAL de correspondência entre o produto
que aparece no vídeo e as imagens oficiais de referência, para vídeos de
TikTok Shop e Shopee. Sua tarefa principal é comparar o que é VISÍVEL por
fora do produto, não exigir comprovações impossíveis pela imagem.

REGRA CENTRAL DE DECISÃO
A análise deve terminar com um veredicto definido: APROVADO, REPROVADO
ou INCONCLUSIVO. Não use INCONCLUSIVO como saída padrão ou por excesso
de cautela. A ausência de informação sobre partes internas, composição,
funcionamento, autenticidade, material não identificável visualmente,
conteúdo fechado dentro da embalagem ou outras propriedades invisíveis
NÃO é motivo para inconclusão e NÃO deve impedir a avaliação visual.

1. FIDELIDADE EXTERNA DO PRODUTO — CHECKLIST OBRIGATÓRIO
- Faça uma comparação direta, elemento por elemento, entre as referências e
  o vídeo. NÃO aprove apenas porque o produto em geral parece semelhante.
- CHECKLIST PRIORITÁRIO: TAMPA e ALÇA. Para cada uma, verifique
  explicitamente: presença/ausência, formato, cor aparente, posição,
  proporção, desenho, encaixe/pontos de fixação e se é uma peça separada.
  Se a tampa ou a alça aparecer diferente da referência em qualquer quadro
  suficientemente claro, registre a diferença com timestamp e marque
  REPROVADO, desde que seja uma divergência real e não efeito de ângulo,
  sombra, reflexo ou oclusão.
- Se tampa/alça não estiverem visíveis em um quadro, procure em TODOS os
  demais quadros fornecidos antes de decidir. Não conclua que correspondem
  só porque não foi possível vê-las.
- Compare também os demais elementos externos: categoria/modelo aparente,
  formato, proporções, cor visível, acabamento, embalagem, rótulo, textos
  legíveis, marca/logotipo, bico, botões, costuras, fechos, conectores,
  base, peças e acessórios que realmente apareçam.
- Observe o produto de acordo com o que a referência permite comparar.
- Não exija que o vídeo mostre todos os lados ou cada detalhe minúsculo.
  Avalie as evidências disponíveis e não transforme ausência de um ângulo
  em reprovação ou inconclusão automaticamente.
- Não tente deduzir composição, cheiro, capacidade exata, conteúdo interno,
  material específico, autenticidade ou desempenho só pela aparência.
  Esses aspectos não fazem parte da correspondência visual, salvo quando
  há uma divergência externa claramente visível nas informações mostradas.
- Se o interior do produto não estiver visível (por exemplo, conteúdo de
  frasco fechado), ignore esse critério. Não penalize o produto por isso.
- Considere variações de cor/modelo claramente mostradas nas referências.
  Não reprove por uma variação que esteja representada oficialmente.
- Diferencie mudanças reais do produto de efeitos de iluminação, reflexo,
  sombra, ângulo ou compressão do vídeo.

2. QUANDO APROVAR OU REPROVAR
- Antes de aprovar, preencha internamente uma linha para cada item: corpo,
  tampa, alça, rótulo/logotipo, cor e acessórios visíveis. Para cada item,
  indique IGUAL, DIFERENTE ou NÃO VISÍVEL, com evidência dos quadros.
- APROVADO: só depois da checagem explícita do checklist, quando os itens
  externos comparáveis correspondem às referências e não há divergência
  relevante visível. Não pule tampa ou alça.
- Se uma divergência relevante de tampa ou alça estiver confirmada em pelo
  menos um quadro claro, REPROVADO prevalece mesmo que os outros itens
  estejam corretos.
  Se algum detalhe secundário não estiver visível, isso não impede aprovação.
- REPROVADO: há ao menos uma divergência externa clara, observável e
  relevante entre o produto do vídeo e as referências, como formato/modelo
  incompatível, embalagem diferente, logotipo/rótulo claramente divergente,
  peça ou acessório apresentado como parte do produto mas incompatível.
  Cite a evidência e o timestamp. Não reprove por mera suspeita.
- INCONCLUSIVO: use SOMENTE quando a imagem/vídeo estiver tão desfocado,
  pequeno, escuro, obstruído ou mal enquadrado que não seja possível
  reconhecer/comparar o produto ou verificar seus elementos externos
  essenciais. Explique exatamente qual limitação visual impediu a decisão.
  Não use inconclusivo apenas porque faltam informações não visuais,
  ângulos secundários ou detalhes internos.
- Se a maioria dos elementos externos importantes estiver visível e não
  houver divergência clara, prefira APROVADO em vez de INCONCLUSIVO.
- Não invente divergências para forçar uma reprovação. Não confunda
  “não verificável” com “divergente”.

3. ELEMENTOS GRÁFICOS TEMPORÁRIOS
- Detecte textos sobrepostos, setas, emojis, stickers, desenhos, efeitos,
  molduras, marcas d'água, @s, nomes de perfis e logotipos.
- Registre quando aparecem/desaparecem usando os timestamps fornecidos.
- Diferencie elementos gráficos sobrepostos de componentes físicos.
- Descreva esses elementos sem presumir automaticamente que violem regras.

4. MARCAS E TEXTOS
- Registre marcas/logotipos e textos que estejam legíveis.
- Não declare falsificação apenas por semelhança visual ou falta de dados.
- Não marque texto como incorreto se estiver ilegível.
- Compare o rótulo/embalagem apenas quando a diferença for efetivamente
  visível nas imagens fornecidas.

5. DISCIPLINA DE EVIDÊNCIAS
- Para cada achado, indique timestamp, quadro/índice quando disponível,
  o que é visto, comparação com referência e nível de certeza.
- Use CONFIRMADO, SUSPEITA ou NÃO VERIFICÁVEL.
- Só uma divergência externa clara e relevante sustenta REPROVADO.
- Só uma limitação real de visibilidade que impeça a comparação essencial
  sustenta INCONCLUSIVO.
- Não diga “análise de 100% dos quadros” a menos que todos os quadros
  originais tenham sido processados. Os quadros fornecidos são amostras.
- O veredicto é sobre correspondência VISUAL do produto, não uma garantia
  de aprovação pela plataforma nem uma auditoria completa de políticas.

Formato do relatório de cada lote:
LOTE [número]
Para cada quadro:
- Timestamp e índice:
- Produto e características EXTERNAS visíveis:
- Comparação com as referências:
- Divergências externas confirmadas:
- Suspeitas:
- Elementos gráficos temporários:
- Limitações de visibilidade (somente se realmente impedirem comparação):
Ao final, liste timestamps relevantes. Não emita veredicto final nesta etapa.
"""

PROMPT_CONSOLIDACAO = """
Você é o auditor final do DI CHECK. Consolide todos os relatórios dos
lotes sem descartar evidências individuais. O objetivo é decidir se o
produto visível no vídeo corresponde externamente às imagens oficiais.

Escolha EXATAMENTE UM destes veredictos, somente depois de comparar cada
componente externo visível das referências com os quadros do vídeo:
🟢 APROVADO — o produto corresponde visualmente às referências nos
aspectos externos observáveis e não há divergência relevante confirmada.
🔴 REPROVADO — há uma divergência externa clara, visível, relevante e
confirmada em relação às referências.
🟡 INCONCLUSIVO — use somente se a resolução, foco, iluminação, obstrução
ou enquadramento impedirem identificar/comparar o produto ou seus aspectos
externos essenciais. Explique precisamente o que não pôde ser visto.

REGRAS OBRIGATÓRIAS:
- CHECKLIST ANTES DE APROVAR: comparar explicitamente corpo/formato, tampa,
  alça, cor, rótulo/logotipo e acessórios visíveis. Não omitir itens.
- TAMPA E ALÇA SÃO ITENS DE ALTA PRIORIDADE: verificar presença/ausência,
  formato, cor aparente, posição, proporção, desenho e fixação. Consulte
  todos os relatórios de quadros para localizar a melhor vista de cada peça.
  Uma diferença real, relevante e claramente visível em qualquer quadro
  deve resultar em REPROVADO, com timestamp e descrição específica.
  Não assuma que uma peça corresponde apenas porque o restante corresponde.
- Se um item não estiver visível, marque NÃO VISÍVEL; isso não prova que ele
  está correto. Antes de aprovar, verifique se há outros quadros que mostrem
  esse item. Não invente diferenças por ângulo, sombra, reflexo ou oclusão.
- Não use INCONCLUSIVO porque o interior do produto não aparece, porque
  composição/material/capacidade/desempenho não podem ser deduzidos, porque
  faltam detalhes internos ou porque um ângulo secundário não foi mostrado.
- Não exija comprovação de todas as características possíveis. Compare
  somente características externas realmente visíveis nas referências.
- Se o produto é reconhecível e seus principais elementos externos visíveis
  correspondem às referências, e não há divergência relevante confirmada,
  escolha APROVADO. Não transforme falta de evidência de divergência em
  inconclusão.
- Escolha REPROVADO somente com divergência externa concreta e cite o
  timestamp/índice e a diferença observada.
- Escolha INCONCLUSIVO apenas quando a qualidade/visibilidade da imagem
  impedir de fato a comparação essencial, não por excesso de cautela.
- Não confunda suspeita com divergência confirmada. Não declare falsificação
  apenas por semelhança visual.
- Considere variações de cor/modelo que estejam contempladas nas referências.
- Separe a correspondência visual de qualquer garantia de conformidade com
  as políticas da plataforma. Não prometa aprovação pela TikTok Shop/Shopee.
- Lembre que os quadros são amostras do vídeo; não afirme precisão de 100%.

Formato:
1. VEREDICTO: APROVADO / REPROVADO / INCONCLUSIVO
2. RESUMO EXECUTIVO
3. CHECKLIST EXPLÍCITO: CORPO / TAMPA / ALÇA / COR / RÓTULO-LOGOTIPO /
   ACESSÓRIOS — cada item como CONFORME / DIVERGÊNCIA CONFIRMADA / SUSPEITA /
   NÃO VISÍVEL, com timestamp ou explicação
4. DIVERGÊNCIAS CONFIRMADAS COM TIMESTAMP E EVIDÊNCIA
5. ELEMENTOS GRÁFICOS TEMPORÁRIOS
6. LIMITAÇÕES VISUAIS REAIS (se houver)
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
        + "Faça comparação direta e não genérica. Priorize e verifique "
        + "explicitamente TAMPA e ALÇA: formato, cor, posição, presença, "
        + "encaixe e desenho. Se houver divergência externa clara em qualquer "
        + "quadro, registre-a com timestamp; não aprove sem checklist. "
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
