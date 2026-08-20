import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
from dados import DADOS_PIX

dash.register_page(__name__, path="/analise", name="Análise de Dados", title="Análise de Dados")

df = DADOS_PIX.copy()
df["Mes"] = df["AnoMes"].dt.strftime("%Y-%m")
df["Milhoes"] = df["ValorPixcontestadosaceitos"] / 1_000_000

total_contestacoes = int(df["QtdePixcontestados"].sum())
total_aceitas = int(df["Qtdecontestacoesaceitas"].sum())
total_valor_aceito = df["ValorPixcontestadosaceitos"].sum()
pct_devolucao_medio = df["PercentualdeDevolucao"].mean()

def kpi(titulo, valor, cor="primary"):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H6(titulo, className="text-muted small mb-1"),
                html.H3(valor, className=f"text-{cor} fw-bold mb-0"),
            ]
        ),
        className="shadow-sm text-center",
    )

fig1 = px.line(
    df, x="Mes",
    y=["Qtdecontestacoesaceitas", "Qtdecontestacoesrejeitadas"],
    markers=True,
    title="Contestações PIX: aceitas vs rejeitadas",
    labels={"value": "Quantidade", "variable": "Situação", "Mes": "Mês"},
)

fig2 = px.bar(
    df, x="Mes", y="Milhoes",
    title="Valor das contestações aceitas (R$ milhões)",
    labels={"Milhoes": "R$ milhões", "Mes": "Mês"},
)

fig3 = px.area(
    df, x="Mes", y="PercentualdeDevolucao",
    title="Percentual de devolução por mês",
    labels={"PercentualdeDevolucao": "% de devolução", "Mes": "Mês"},
)

total_devolvido = df["ValorPixdevolvidosintegralmente"].sum()
total_nao_devolvido = df["ValorPixresidualnaodevolvido"].sum()
fig4 = px.pie(
    names=["Devolvido integralmente (MED)", "Valor residual não devolvido"],
    values=[total_devolvido, total_nao_devolvido],
    title="Destino dos valores contestados (total do período)",
)

for fig in [fig1, fig2, fig3, fig4]:
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")

def fmt_br(v):
    return f"R$ {v:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

layout = dbc.Container(
    [
        html.H2("Análise de Dados", className="mb-1 fw-bold"),
        html.P("Fraudes e contestações PIX — dados abertos do Banco Central", className="text-muted mb-4"),
        dbc.Row(
            [
                dbc.Col(kpi("Contestações (total)", f"{total_contestacoes:,.0f}".replace(",", ".")), md=3),
                dbc.Col(kpi("Aceitas", f"{total_aceitas:,.0f}".replace(",", "."), "success"), md=3),
                dbc.Col(kpi("Valor aceito", fmt_br(total_valor_aceito), "info"), md=3),
                dbc.Col(kpi("% devolução médio", f"{pct_devolucao_medio:.2f}%", "warning"), md=3),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig1), md=6, className="mb-4"),
                dbc.Col(dcc.Graph(figure=fig2), md=6, className="mb-4"),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig3), md=6, className="mb-4"),
                dbc.Col(dcc.Graph(figure=fig4), md=6, className="mb-4"),
            ]
        ),
    ],
    className="py-3",
)