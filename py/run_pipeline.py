from rss import coletar_rss
from openai_agent import analisar_texto
from storage import salvar_oportunidade
from datetime import datetime
import json

# ✅ NOVO IMPORT (EMAIL)
from email_sender import enviar_email

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

    # ✅ LISTA NOVA (NÃO ALTERA NADA DO RESTO)
    novas_lista = []

    for item in itens:

        print(f"🔄 analisando: {item.get('titulo','')[:60]}...")

        texto = f"{item.get('titulo','')} {item.get('texto','')}".lower()

        # ✅ filtro simples
        if not any(t in texto for t in TERMOS_ELEGIVEIS):
            continue

        # ✅ limite de uso da IA
        if analises >= MAX_ANALISES_IA:
            continue

        # ✅ IA protegida contra travamento
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

            # ✅ ADIÇÃO (GUARDA PRA EMAIL)
            novas_lista.append(oportunidade)

            print("✅ Nova:", oportunidade.get("titulo"))

    # ✅ ENVIA EMAIL (SÓ SE TIVER NOVAS)
    if novas_lista:
        enviar_email(novas_lista)

    # ✅ salva data (mantém seu app funcionando)
    with open("ultima_atualizacao.json", "w", encoding="utf-8") as f:
        json.dump(
            {"ultima_atualizacao": datetime.now().strftime("%d/%m/%Y %H:%M")},
            f
        )

    print(f"✅ Finalizado | IA usadas: {analises} | Novas: {novas}")


if __name__ == "__main__":
    executar_pipeline()