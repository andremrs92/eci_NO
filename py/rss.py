import feedparser
from datetime import datetime, timedelta
import urllib.parse


DOMINIOS_INSTITUCIONAIS = [
    "bndes.gov.br",
    "gov.br",
    "sp.gov.br",
    "rj.gov.br",
    "mg.gov.br",
    "rs.gov.br",
    "sc.gov.br",
    "pr.gov.br",
    "ba.gov.br",
]

TERMOS_PPP = [
    "parceria público privada",
    "PPP",
    "concessão",
    "parceria com o setor privado",
]


def coletar_rss(dias=30):
    resultados = []
    data_limite = datetime.now() - timedelta(days=dias)

    for dominio in DOMINIOS_INSTITUCIONAIS:
        for termo in TERMOS_PPP:

            query = urllib.parse.quote(f"{termo} site:{dominio}")

            url = (
                "https://news.google.com/rss/search?"
                f"q={query}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
            )

            feed = feedparser.parse(url)

            if feed.bozo:
                continue

            for entry in feed.entries:
                data = _parse_data(entry)

                if data < data_limite:
                    continue

                resultados.append({
                    "titulo": entry.get("title", ""),
                    "texto": entry.get("summary", ""),
                    "link": entry.get("link", ""),
                    "data_publicacao": data.strftime("%Y-%m-%d"),
                    "fonte": dominio,
                })

    return resultados


def _parse_data(entry):
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime(*entry.published_parsed[:6])
    return datetime.now()