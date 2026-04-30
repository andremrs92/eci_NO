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
        return datetime.min


def formatar_data(d):
    try:
        data = datetime.strptime(d.get("data_publicacao", ""), "%Y-%m-%d")
        return data.strftime("%d/%m/%Y")
    except:
        return "-"


def filtrar_por_data(dados, periodo):
    hoje = datetime.now()

    if periodo == "Hoje":
        return [d for d in dados if (hoje - parse_data(d)).days == 0]

    if periodo == "Últimos 7 dias":
        return [d for d in dados if (hoje - parse_data(d)).days <= 7]

    if periodo == "Últimos 30 dias":
        return [d for d in dados if (hoje - parse_data(d)).days <= 30]

    if periodo == "Mais antigos":
        return [d for d in dados if (hoje - parse_data(d)).days > 30]

    return dados


def extrair_mes_ano(d):
    data = parse_data(d)
    return data.strftime("%B %Y")  # ex: April 2026


# -----------------------------
# Interface
# -----------------------------
st.set_page_config(page_title="Radar de PPP & Concessões", layout="wide")

st.title("📡 Radar de Projetos de PPP's & Concessões")
st.caption("🔒 Dados atualizados pelo sistema interno")

dados = carregar_dados()

# ✅ Ordena por data (mais recente primeiro)
dados = sorted(dados, key=parse_data, reverse=True)

# -----------------------------
# FILTROS
# -----------------------------

# 🔹 Filtro rápido
periodo = st.selectbox(
    "Período",
    ["Todos", "Hoje", "Últimos 7 dias", "Últimos 30 dias", "Mais antigos"]
)

# 🔹 Filtro por mês (🔥 principal melhoria)
meses = sorted(
    set(extrair_mes_ano(d) for d in dados),
    reverse=True
)

mes_selecionado = st.selectbox("Mês", ["Todos"] + meses)

# 🔹 Filtro por setor (mantido)
setores = sorted(set(d.get("setor", "Outro") for d in dados))
setor = st.selectbox("Setor", ["Todos"] + setores)

# -----------------------------
# Aplicação dos filtros
# -----------------------------

dados_filtrados = list(dados)

# setor
if setor != "Todos":
    dados_filtrados = [d for d in dados_filtrados if d.get("setor") == setor]

# período
dados_filtrados = filtrar_por_data(dados_filtrados, periodo)

# mês
if mes_selecionado != "Todos":
    dados_filtrados = [
        d for d in dados_filtrados
        if extrair_mes_ano(d) == mes_selecionado
    ]

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
            f"📅 {formatar_data(d)} | {d.get('setor')} | Estágio: {d.get('estagio')}"
        )

        st.write(d.get("resumo"))

        if d.get("link"):
            st.link_button("Ver fonte", d.get("link"))

        st.divider()
