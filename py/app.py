import streamlit as st
import json
import os
from datetime import datetime

ARQUIVO = "oportunidades.json"

# -----------------------------
# Utilidades
# -----------------------------
def carregar_dados():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_data(d):
    try:
        return datetime.strptime(d.get("data_publicacao", ""), "%Y-%m-%d")
    except Exception:
        return datetime.now()


def filtrar_por_data(dados, periodo):
    hoje = datetime.now()

    if periodo == "Hoje":
        return [d for d in dados if (hoje - parse_data(d)).days == 0]

    if periodo == "Últimos 7 dias":
        return [d for d in dados if (hoje - parse_data(d)).days <= 7]

    if periodo == "Últimos 30 dias":
        return [d for d in dados if (hoje - parse_data(d)).days <= 30]

    return dados


# -----------------------------
# Interface
# -----------------------------
st.set_page_config(page_title="Radar de PPP & Concessões", layout="wide")

st.title("📡 Radar de Projetos de PPP & Concessões")
st.caption("🔒 Dados atualizados pelo sistema interno")

dados = carregar_dados()

# -----------------------------
# Filtros
# -----------------------------
setores = sorted(set(d.get("setor", "Outro") for d in dados))
setor = st.selectbox("Setor", ["Todos"] + setores)

periodo = st.selectbox(
    "Período",
    ["Todos", "Hoje", "Últimos 7 dias", "Últimos 30 dias"]
)

dados_filtrados = list(dados)

if setor != "Todos":
    dados_filtrados = [d for d in dados_filtrados if d.get("setor") == setor]

dados_filtrados = filtrar_por_data(dados_filtrados, periodo)

st.divider()

# -----------------------------
# Lista de oportunidades
# -----------------------------
if not dados_filtrados:
    st.info("Nenhuma oportunidade encontrada para os filtros selecionados.")
else:
    for d in dados_filtrados:
        st.subheader(d.get("titulo"))
        st.caption(
            f"{d.get('setor')} | Estágio: {d.get('estagio')} | Relevância: {d.get('relevancia')}"
        )
        st.write(d.get("resumo"))
        if d.get("link"):
            st.link_button("Ver fonte", d.get("link"))
        st.divider()
