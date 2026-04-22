import json
import os

ARQUIVO_STORAGE = "oportunidades.json"


def carregar_oportunidades():
    if not os.path.exists(ARQUIVO_STORAGE):
        return []

    with open(ARQUIVO_STORAGE, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_todas_oportunidades(oportunidades):
    with open(ARQUIVO_STORAGE, "w", encoding="utf-8") as f:
        json.dump(oportunidades, f, ensure_ascii=False, indent=2)


def ja_existe_hash(hash_item: str) -> bool:
    """
    Verifica se uma notícia (hash) já foi analisada antes.
    Evita reanalisar e gastar IA desnecessariamente.
    """
    oportunidades = carregar_oportunidades()

    for op in oportunidades:
        if op.get("hash") == hash_item:
            return True

    return False


def salvar_oportunidade(oportunidade: dict) -> bool:
    """
    Salva oportunidade apenas se ainda não existir.
    Retorna True se salvou, False se já existia.
    """
    oportunidades = carregar_oportunidades()

    # Evita duplicação por URL
    for op in oportunidades:
        if op.get("link") == oportunidade.get("link"):
            return False

    oportunidades.append(oportunidade)
    salvar_todas_oportunidades(oportunidades)

    return True