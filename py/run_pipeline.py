from rss import coletar_rss
from openai_agent import analisar_texto
from storage import salvar_oportunidade
from datetime import datetime
import json

MAX_ANALISES_IA = 50
MODO_SECO = False

TERMOS_ELEGIVEIS = [
    "ppp",
    "parceria",
    "concess",
    "setor privado",
    "parceiro privado",
]


# -----------------------------
# ✅ DEDUPLICAÇÃO (ADIÇÃO)
# -----------------------------
def normalizar_texto(texto):
    if not texto:
        return ""
    
    texto = texto.lower().strip()

    for c in [".", ",", "-", ":", ";", "(", ")", "'"]:
        texto = texto.replace(c, "")

    return texto


def remover_duplicados(itens):
    vistos = set()
    resultado = []

    for item in itens:
        titulo_limpo = normalizar_texto(item.get("titulo", ""))

        if titulo_limpo in vistos:
            continue

        vistos.add(titulo_limpo)
        resultado.append(item)

    return resultado


# -----------------------------
# 🚀 PIPELINE
# -----------------------------
def executar_pipeline():
    print("🔎 Radar iniciado")

    # ✅ coleta
    itens = coletar_rss(dias=30)

    print(f"📄 {len(itens)} itens coletados")

    # ✅ REMOVE DUPLICADOS AQUI (PONTO CERTO)
    itens = remover_duplicados(itens)

    print(f"🧹 {len(itens)} únicos")

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

    # ✅ salva última atualização (já estava)
    with open("ultima_atualizacao.json", "w", encoding="utf-8") as f:
        json.dump(
            {"ultima_atualizacao": datetime.now().strftime("%d/%m/%Y %H:%M")},
            f
        )

    print(f"✅ Finalizado | IA usadas: {analises} | Novas: {novas}")


if __name__ == "__main__":
    executar_pipeline()