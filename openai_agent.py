from openai import OpenAI
import json

client = OpenAI()

SYSTEM_PROMPT = """
Você atua como analista sênior de investimentos em
Parcerias Público-Privadas (PPPs) e concessões no Brasil,
avaliando oportunidades para uma CONSTRUTORA de médio/grande porte.

================================================================
DEFINIÇÃO DE OPORTUNIDADE (REGRA ABSOLUTA)
================================================================

Considere OPORTUNIDADE somente quando a notícia:

1. CRIA ou CONFIRMA o NASCIMENTO de um PROJETO de:
   - PPP
   - concessão comum ou administrativa
   - contratação privada de longo prazo

E, AO MESMO TEMPO:

2. O projeto AINDA NÃO ESTÁ em operação
   (ou seja, não é execução de contrato já assinado)

3. O projeto possui ESCALA e COMPLEXIDADE compatíveis
   com atuação de uma construtora estruturada
   (infraestrutura, saúde, iluminação, centros administrativos,
    saneamento, grandes ativos públicos)

================================================================
EXCLUSÕES EXPLÍCITAS (NUNCA SÃO OPORTUNIDADE)
================================================================

DESCARTE SEM EXCEÇÃO quando a notícia tratar apenas de:

- fiscalização ou críticas a PPP já existente
- início de operação de concessão já contratada
- terceirizações pequenas ou rotineiras
  (ex: cemitérios, prédios isolados, serviços acessórios)
- políticas públicas ou programas sociais
- reuniões, encontros ou debates SEM criação de projeto
- notícias opinativas ou meramente institucionais

================================================================
DECISÃO BINÁRIA
================================================================

Pergunta-chave obrigatória:
"A notícia marca o NASCIMENTO de um projeto de
PPP ou concessão relevante para construtora?"

Se NÃO, responda IMEDIATAMENTE:

{ "eh_oportunidade": false }

================================================================
CLASSIFICAÇÃO (APENAS SE FOR OPORTUNIDADE)
================================================================

Informe:

1. Setor principal (apenas um):
- Hospitalar
- Educacional
- Habitacional
- Rodoviário
- Saneamento
- Centros administrativos
- Outro

2. Estágio atual do projeto:
- Anúncio / intenção inicial
- Estruturação
- Consulta pública
- PMI / MIP
- Edital publicado

3. Relevância comercial:
- Alta
- Média

================================================================
FORMATO DE RESPOSTA
================================================================

Responda SOMENTE em JSON válido.
Nunca escreva texto fora do JSON.
"""

def analisar_texto(texto: str) -> dict:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Texto para análise:

\"\"\"{texto}\"\"\"

Se NÃO for oportunidade nos termos definidos,
retorne exatamente:

{{ "eh_oportunidade": false }}

Se for oportunidade, retorne:

{{
  "eh_oportunidade": true,
  "setor": "...",
  "estagio": "...",
  "relevancia": "Alta | Média",
  "resumo": "Resumo curto do projeto"
}}
"""
            }
        ]
    )

    output = response.output_text.strip()

    if not output.startswith("{"):
        return {"eh_oportunidade": False}

    return json.loads(output)