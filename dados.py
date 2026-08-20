# 
# DADOS PESSOAIS — edite tudo aqui e o dashboard inteiro muda
# 

import json
import os
import pandas as pd

_BASE_DIR = os.path.dirname(__file__)
_CAMINHO_PIX = os.path.join(_BASE_DIR, "dados", "pix_fraudes.json")

with open(_CAMINHO_PIX, encoding="utf-8") as _f:
    _dados_pix = json.load(_f)

DADOS_PIX = pd.DataFrame(_dados_pix["value"])
DADOS_PIX["AnoMes"] = pd.to_datetime(DADOS_PIX["AnoMes"].astype(str), format="%Y%m")
DADOS_PIX = DADOS_PIX.sort_values("AnoMes").reset_index(drop=True)

PESSOA = {
    "nome": "Lucas Mesquita Massoni",
    "cargo": "Estudante de Engenharia de Software",
    "cidade": "São Paulo - SP",
    "email": "lucas.masson0307@email.com",
    "linkedin": "https://www.linkedin.com/in/lucas-massoni-393968357/",
    "minibio": (
        "Sou Lucas, 19 anos, estudante de Engenharia de Software na FIAP (4º semestre). "
        "Meu interesse por tecnologia vem da robótica no colégio. Foco em Python, SQL e "
        "análise de dados com pandas, com projetos práticos em dados e IA. "
        "Busco estágio em tecnologia para crescer junto com uma empresa em expansão."
    ),
    "formacao": [
        {"curso": "Engenharia de Software (4º semestre)",
         "instituicao": "FIAP", "ano": "2025 - 2028"},
    ],
    "cases": [
        {
            "titulo": "Análise do impacto de cartões vermelhos no Brasileirão",
            "resumo": "Coletamos manualmente dados de mais de 700 partidas (placar, "
                      "minutagem dos cartões, gols, faltas, juízes) e, com SQL + Streamlit, "
                      "geramos tabelas e gráficos para entender o impacto no resultado.",
            "resultado": "Conclusão: cartão no 1º tempo = 60% de chance de virada do time com um a mais",
        },
        {
            "titulo": "Plataforma com IA para a TOTVS",
            "resumo": "Projeto avançado que lê transcrições de reuniões e centraliza análises "
                      "e gráficos para aumentar a produtividade e efetividade das equipes.",
            "resultado": "Impacto: automação de análises e ganho de produtividade",
        },
    ],
}

CURSOS = [
    {"nome": "Python para Análise de Dados", "instituicao": "FIAP + estudos próprios",
     "carga": "2 anos de prática", "ano": "2024 - atual", "certificado": "https://link-do-certificado"},
    {"nome": "SQL e Banco de Dados", "instituicao": "FIAP",
     "carga": "em andamento", "ano": "2025", "certificado": "https://link-do-certificado"},
    {"nome": "Estatística aplicada com pandas", "instituicao": "FIAP",
     "carga": "em andamento", "ano": "2025", "certificado": "https://link-do-certificado"},
]

SKILLS = {
    "Linguagens": [("Python", 90), ("SQL", 80), ("Java", 65), ("HTML/CSS", 70)],
    "Ferramentas": [("pandas", 80), ("Streamlit", 75), ("Git", 60)],
    "Soft Skills": [("Raciocínio lógico", 92), ("Dedicação", 90),
                    ("Atenção aos detalhes", 88)],
}