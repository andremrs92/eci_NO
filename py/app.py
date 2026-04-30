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


def extrair_mes_ano(d):
    data = parse_data(d)

    meses_pt = {
        "January": "Janeiro",
        "February": "Fevereiro",
        "March": "Março",
        "April": "Abril",
        "May": "Maio",
        "June": "Junho",
        "July": "Julho",
        "August": "Agosto",
        "September": "Setembro",
        "October": "Outubro",
        "November": "Novembro",
        "December": "Dezembro",
    }

    mes_en = data.strftime("%B")
    mes_pt = meses_pt.get(mes_en, mes_en)

    return f"{mes_pt} {data.year}"


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


# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="Radar PPP", layout="wide")

st.title("📡 Radar de Projetos de PPP's & Concessões")
st.caption("🔒 Dados atualizados pelo sistema interno")

dados = carregar_dados()

# ✅ ordena
dados = sorted(dados, key=parse_data, reverse=True)


# -----------------------------
# Filtros
# -----------------------------

periodo = st.selectbox(
    "Período",
    ["Todos", "Hoje", "Últimos 7 dias", "Últimos 30 dias", "Mais antigos"]
)

meses = sorted(set(extrair_mes_ano(d) for d in dados), reverse=True)
mes_selecionado = st.selectbox("Mês", ["Todos"] + meses)

setores = sorted(set(d.get("setor", "Outro") for d in dados))
setor = st.selectbox("Setor", ["Todos"] + setores)

dados_filtrados = list(dados)

if setor != "Todos":
    dados_filtrados = [d for d in dados_filtrados if d.get("setor") == setor]

dados_filtrados = filtrar_por_data(dados_filtrados, periodo)

if mes_selecionado != "Todos":
    dados_filtrados = [
        d for d in dados_filtrados
        if extrair_mes_ano(d) == mes_selecionado
    ]

st.divider()


# -----------------------------
# LISTA
# -----------------------------
if not dados_filtrados:
    st.info("Nenhuma oportunidade encontrada.")
else:
    for d in dados_filtrados:

        # ✅ IMAGEM
        if d.get("imagem"):
            st.image(d.get("imagem"), use_container_width=True)

        st.subheader(d.get("titulo"))

        st.caption(
            f"📅 {formatar_data(d)} | {d.get('setor')} | Estágio: {d.get('estagio')}"
        )

        st.write(d.get("resumo"))

        if d.get("link"):
            st.link_button("Ver fonte", d.get("link"))

        st.divider()
