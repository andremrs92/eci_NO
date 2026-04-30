from rss import coletar_rss
from news_aggregator import coletar_noticias_agregador
from openai_agent import analisar_texto
from storage import salvar_oportunidade


MAX_ANALISES_IA = 50   # ponto ótimo
MODO_SECO = False     # True só quando estiver testando UI/fonte


TERMOS_ELEGIVEIS = [
    "ppp",
    "parceria",
    "concess",
    "setor privado",
    "parceiro privado",
]

# -----------------------------
# 🧠 DEDUPLICAÇÃO
# -----------------------------
def normalizar_texto(texto):
    return texto.lower().strip() if texto else ""


def remover_duplicados(itens):
    vistos = set()
    resultado = []

    for item in itens:
        titulo = normalizar_texto(item.get("titulo", ""))

        # chave baseada no título
        chave = titulo

        if chave in vistos:
            continue

        vistos.add(chave)
        resultado.append(item)

    return resultado


# -----------------------------
# 🚀 PIPELINE
# -----------------------------
def executar_pipeline():
    print("🔎 Radar de descoberta iniciado")

    itens = []
    itens += coletar_rss(dias=30)
    itens += coletar_noticias_agregador(dias=30)

    print(f"📄 {len(itens)} itens coletados")

    # ✅ REMOVE DUPLICADOS ANTES DA IA
    itens = remover_duplicados(itens)

    print(f"🧹 Após deduplicação: {len(itens)} itens únicos")

    analises = 0
    novas = 0

    for item in itens:
        texto = f"{item.get('titulo','')} {item.get('texto','')}"
        texto_lower = texto.lower()

        # ✅ Pré-filtro SIMPLES (só elegibilidade)
        if not any(t in texto_lower for t in TERMOS_ELEGIVEIS):
            continue

        # ✅ Limite controlado de IA
        if analises >= MAX_ANALISES_IA:
            continue

        if MODO_SECO:
            analise = {"eh_oportunidade": False}
        else:
            analise = analisar_texto(texto)
            analises += 1

        if not analise.get("eh_oportunidade"):
            continue

        oportunidade = {
            **item,
            **analise
        }

        if salvar_oportunidade(oportunidade):
            novas += 1
            print("✅ Nova oportunidade:", oportunidade.get("titulo"))

    print(f"✅ Finalizado | IA usadas: {analises} | Novas: {novas}")


if __name__ == "__main__":
    executar_pipeline()
