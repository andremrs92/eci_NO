import streamlit as st
import json
import os
from datetime import datetime, timedelta
import subprocess

ARQUIVO = "oportunidades.json"

def carregar():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def parse(d):
    try:
        return datetime.strptime(d["data_publicacao"], "%Y-%m-%d")
    except:
        return datetime.now()

def filtro_data(dados, periodo):
    hoje = datetime.now()
    if periodo == "Hoje":
        return [d for d in dados if (hoje - parse(d)).days == 0]
    if periodo == "Últimos 7 dias":
        return [d for d in dados if (hoje - parse(d)).days <= 7]
    if periodo == "Últimos 30 dias":
        return [d for d in dados if (hoje - parse(d)).days <= 30]
    return dados

st.set_page_config(layout="wide")
st.title("📡 Radar de Projetos de PPP & Concessões")

if st.button("🔎 BUSCAR NOVOS PROJETOS"):
    with st.spinner("Executando pipeline…"):
        subprocess.run(["python", "run_pipeline.py"], check=True)
    st.success("✅ Atualizado")
    st.rerun()

dados = carregar()
dados_f = list(dados)

setor = st.selectbox("Setor", ["Todos"] + sorted(set(d.get("setor","Outro") for d in dados)))
periodo = st.selectbox("Período", ["Todos","Hoje","Últimos 7 dias","Últimos 30 dias"])

if setor != "Todos":
    dados_f = [d for d in dados_f if d.get("setor") == setor]

dados_f = filtro_data(dados_f, periodo)

st.divider()

for d in dados_f:
    st.subheader(d.get("titulo"))
    st.caption(
        f"{d.get('setor')} | Estágio: {d.get('estagio')} | Relevância: {d.get('relevancia')}"
    )
    st.write(d.get("resumo"))
    st.link_button("Fonte", d.get("link"))
    st.divider()