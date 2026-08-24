import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
import plotly.express as px
from dados import DADOS_PIX

dash.register_page(__name__, path="/analise", name="Análise de Dados", title="Análise de Dados")

df = DADOS_PIX.copy()
df["Mes"] = df["AnoMes"].dt.strftime("%Y-%m")
df["Ano"] = df["AnoMes"].dt.year
anos = sorted(df["Ano"].unique())

# ---------- Layout ----------
layout = dbc.Container(
    [
        html.H2("Análise de Dados", className="mb-1 fw-bold"),
        html.P("Fraudes e contestações PIX — dados abertos do Banco Central", className="text-muted mb-3"),
        dbc.Row(
            dbc.Col(
                [
                    html.Label("Filtrar por ano:", className="fw-semibold me-2"),
                    dcc.Dropdown(
                        id="filtro-ano",
                        options=[{"label": str(a), "value": a} for a in anos],
                        value=None,
                        placeholder="Todos os anos",
                        clearable=True,
                        style={"width": "220px", "display": "inline-block"},
                    ),
                ],
                className="mb-3",
            )
        ),
        html.Div(id="kpis"),
        html.Div(id="graficos"),
    ],
    className="py-3",
)

# ---------- Callbacks ----------
@dash.callback(
    Output("kpis", "children"),
    Output("graficos", "children"),
    Input("filtro-ano", "value"),
)
def atualizar(ano):
    d = df if ano is None else df[df["Ano"] == ano]

    total_contest = int(d["QtdePixcontestados"].sum())
    total_aceitas = int(d["Qtdecontestacoesaceitas"].sum())
    total_rejeitadas = int(d["Qtdecontestacoesrejeitadas"].sum())
    total_valor_aceito = d["ValorPixcontestadosaceitos"].sum()
    total_valor_devolvido = d["ValorPixdevolvidosintegralmente"].sum()
    total_chaves_fraude = int(d["QtdeChavesPixcommarcacoesdefraude"].sum())
    total_bloqueios = int(d["QtdePixbloqueadoscautelarmenteeliberados"].sum())
    pct_medio = d["PercentualdeDevolucao"].mean()

    def kpi(titulo, valor, cor="primary", icone="bi-graph-up"):
        return dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [html.I(className=f"bi {icone} me-2"), html.Span(titulo, className="text-muted small")],
                        className="mb-1",
                    ),
                    html.H4(valor, className=f"text-{cor} fw-bold mb-0"),
                ]
            ),
            className="shadow-sm",
        )

    def fmt_br(v):
        return f"R$ {v:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

    kpis = dbc.Row(
        [
            dbc.Col(kpi("Contestações", f"{total_contest:,.0f}".replace(",", "."), "primary", "bi-arrow-repeat"), md=3, className="mb-3"),
            dbc.Col(kpi("Aceitas", f"{total_aceitas:,.0f}".replace(",", "."), "success", "bi-check-circle"), md=3, className="mb-3"),
            dbc.Col(kpi("Rejeitadas", f"{total_rejeitadas:,.0f}".replace(",", "."), "danger", "bi-x-circle"), md=3, className="mb-3"),
            dbc.Col(kpi("Valor aceito", fmt_br(total_valor_aceito), "info", "bi-cash-stack"), md=3, className="mb-3"),
            dbc.Col(kpi("Valor devolvido", fmt_br(total_valor_devolvido), "success", "bi-arrow-left-circle"), md=3, className="mb-3"),
            dbc.Col(kpi("Chaves em fraude", f"{total_chaves_fraude:,.0f}".replace(",", "."), "warning", "bi-shield-exclamation"), md=3, className="mb-3"),
            dbc.Col(kpi("Bloqueios cautelares", f"{total_bloqueios:,.0f}".replace(",", "."), "secondary", "bi-lock"), md=3, className="mb-3"),
            dbc.Col(kpi("% devolução médio", f"{pct_medio:.2f}%", "primary", "bi-percent"), md=3, className="mb-3"),
        ]
    )

    # ---- Gráficos ----
    fig1 = px.line(
        d, x="Mes",
        y=["Qtdecontestacoesaceitas", "Qtdecontestacoesrejeitadas"],
        markers=True,
        title="Aceitas vs Rejeitadas",
        labels={"value": "Quantidade", "variable": "Situação", "Mes": "Mês"},
    )

    d2 = d.copy()
    d2["Valor aceito (R$ mi)"] = d2["ValorPixcontestadosaceitos"] / 1_000_000
    d2["Valor devolvido (R$ mi)"] = d2["ValorPixdevolvidosintegralmente"] / 1_000_000
    fig2 = px.bar(
        d2, x="Mes",
        y=["Valor aceito (R$ mi)", "Valor devolvido (R$ mi)"],
        barmode="group",
        title="Valores em R$ milhões por mês",
        labels={"value": "R$ milhões", "variable": "Tipo", "Mes": "Mês"},
    )

    fig3 = px.area(
        d, x="Mes", y="PercentualdeDevolucao",
        title="Percentual de devolução",
        labels={"PercentualdeDevolucao": "% devolução", "Mes": "Mês"},
    )

    fig4 = px.bar(
        d, x="Mes", y="QtdeChavesPixcommarcacoesdefraude",
        title="Chaves PIX marcadas como fraude",
        labels={"QtdeChavesPixcommarcacoesdefraude": "Chaves", "Mes": "Mês"},
        color_discrete_sequence=["#ffc107"],
    )

    d3 = d.copy()
    d3["MED (R$ mi)"] = d3["ValorPixdevolvidosintegralmente"] / 1_000_000
    fig5 = px.bar(
        d3, x="Mes", y="QuantidadedevolvidaintegralmentepormeiodoMED",
        title="Devoluções via MED (quantidade)",
        labels={"QuantidadedevolvidaintegralmentepormeiodoMED": "Quantidade", "Mes": "Mês"},
        color_discrete_sequence=["#20c997"],
    )

    fig6 = px.bar(
        d, x="Mes",
        y=["QtdePixbloqueadoscautelarmenteeliberados", "QtdePixbloqueadoscautelarmenteedevolvidos"],
        barmode="group",
        title="Bloqueios cautelares: liberados vs devolvidos",
        labels={"value": "Quantidade", "variable": "Tipo", "Mes": "Mês"},
    )

    total_nao_devolvido = d["ValorPixresidualnaodevolvido"].sum()
    fig7 = px.pie(
        names=["Devolvido integralmente (MED)", "Valor residual não devolvido"],
        values=[total_valor_devolvido, total_nao_devolvido],
        title="Destino dos valores contestados",
    )

    fig8 = px.scatter(
        d, x="QtdePixcontestados", y="PercentualdeDevolucao",
        hover_name="Mes",
        title="Relação: volume de contestações vs % devolução",
        labels={"QtdePixcontestados": "Contestações", "PercentualdeDevolucao": "% devolução"},
    )

    for fig in [fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8]:
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")

    graficos = dbc.Container(
        [
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
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=fig5), md=6, className="mb-4"),
                    dbc.Col(dcc.Graph(figure=fig6), md=6, className="mb-4"),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=fig7), md=6, className="mb-4"),
                    dbc.Col(dcc.Graph(figure=fig8), md=6, className="mb-4"),
                ]
            ),
        ]
    )

    return kpis, graficos