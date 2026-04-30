from rss import coletar_rss
from news_aggregator import coletar_noticias_agregador
from openai_agent import analisar_texto
from storage import salvar_oportunidade


MAX_ANALISES_IA = 50
MODO_SECO = False

TERMOS_ELEGIVEIS = [
    "ppp",
    "parceria",
    "concess",
    "setor privado",
    "parceiro privado",
]


def executar_pipeline():
    print("🔎 Radar iniciado")

    itens = []
    itens += coletar_rss(dias=30)
    itens += coletar_noticias_agregador(dias=30)

    print(f"📄 {len(itens)} itens coletados")

    analises = 0
    novas = 0

    for item in itens:
        texto = f"{item.get('titulo','')} {item.get('texto','')}".lower()

        if not any(t in texto for t in TERMOS_ELEGIVEIS):
            continue

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
            print("✅ Nova:", oportunidade.get("titulo"))

    print(f"✅ Finalizado | IA usadas: {analises} | Novas: {novas}")


if __name__ == "__main__":
    executar_pipeline()