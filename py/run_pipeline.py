from rss import coletar_rss
from openai_agent import analisar_texto
from storage import salvar_oportunidade
from datetime import datetime
import json

MAX_ANALISES_IA = 50

TERMOS_ELEGIVEIS = [
    "ppp",
    "parceria",
    "concess",
    "setor privado",
    "parceiro privado",
]


def executar_pipeline():
    print("🔎 Radar iniciado")

    itens = coletar_rss(dias=30)

    print(f"📄 {len(itens)} itens coletados")

    analises = 0
    novas = 0

    novas_lista = []

    for item in itens:

        print(f"🔄 analisando: {item.get('titulo','')[:60]}...")

        texto = f"{item.get('titulo','')} {item.get('texto','')}".lower()

        if not any(t in texto for t in TERMOS_ELEGIVEIS):
            continue

        if analises >= MAX_ANALISES_IA:
            continue

        try:
            analise = analisar_texto(texto)
            analises += 1
        except:
            print("⚠️ erro na IA, pulando...")
            continue

        if not analise.get("eh_oportunidade"):
            continue

        oportunidade = {
            **item,
            **analise
        }

        if salvar_oportunidade(oportunidade):
            novas += 1

            novas_lista.append(oportunidade)

            print("✅ Nova:", oportunidade.get("titulo"))


    with open("ultima_atualizacao.json", "w", encoding="utf-8") as f:
        json.dump(
            {"ultima_atualizacao": datetime.now().strftime("%d/%m/%Y %H:%M")},
            f
        )

    print(f"✅ Finalizado | IA usadas: {analises} | Novas: {novas}")


if __name__ == "__main__":
    executar_pipeline()