import streamlit as st
import json
import os
from datetime import datetime

ARQUIVO = "oportunidades.json"


# -----------------------------
# Utils
# -----------------------------
def carregar_dados():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def carregar_ultima_atualizacao():
    try:
        with open("ultima_atualizacao.json", "r", encoding="utf-8") as f:
            return json.load(f).get("ultima_atualizacao")
    except:
        return None


def parse_data(d):
    try:
        return datetime.strptime(d.get("data_publicacao", ""), "%Y-%m-%d")
    except:
        return datetime.min


def formatar_data(d):
    try:
        data = datetime.strptime(d.get("data_publicacao", ""), "%Y-%m-%d")
        return data.strftime("%d/%m/%Y")
    except:
        return "-"


# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="Radar PPP", layout="wide")

st.title("📡 Radar de Projetos de PPP's & Concessões")

ultima = carregar_ultima_atualizacao()

if ultima:
    st.caption(f"🔒 Dados atualizados pelo sistema interno • Última atualização: {ultima}")
else:
    st.caption("🔒 Dados atualizados pelo sistema interno")

dados = carregar_dados()

# ordena
dados = sorted(dados, key=parse_data, reverse=True)

st.divider()

# -----------------------------
# LISTA
# -----------------------------
if not dados:
    st.info("Nenhuma oportunidade encontrada.")
else:
    for d in dados:

        st.subheader(d.get("titulo"))

        st.caption(
            f"📅 {formatar_data(d)} | {d.get('setor')} | Estágio: {d.get('estagio')}"
        )

        st.write(d.get("resumo"))

        if d.get("link"):
            st.link_button("Ver fonte", d.get("link"))

        st.divider()