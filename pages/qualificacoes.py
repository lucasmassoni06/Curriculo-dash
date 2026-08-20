import dash
import dash_bootstrap_components as dbc
from dash import html
from dados import CURSOS

dash.register_page(__name__, path="/qualificacoes", name="Qualificações", title="Qualificações")

rows = [
    html.Tr(
        [
            html.Td(c["nome"]),
            html.Td(c["instituicao"]),
            html.Td(c["carga"]),
            html.Td(c["ano"]),
            html.Td(html.A("Ver certificado", href=c["certificado"], target="_blank")),
        ]
    )
    for c in CURSOS
]

layout = dbc.Container(
    [
        html.H2("Qualificações", className="mb-1 fw-bold"),
        html.P("Cursos e certificados", className="text-muted mb-4"),
        dbc.Table(
            [
                html.Thead(html.Tr([html.Th("Curso"), html.Th("Instituição"), html.Th("Carga"), html.Th("Ano"), html.Th("Certificado")])),
                html.Tbody(rows),
            ],
            striped=True,
            bordered=True,
            hover=True,
            responsive=True,
        ),
    ],
    className="py-3",
)