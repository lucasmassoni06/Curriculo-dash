import dash
import dash_bootstrap_components as dbc
from dash import html
from dados import SKILLS

dash.register_page(__name__, path="/skills", name="Skills", title="Skills")

def skill_group(titulo, itens):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(titulo, className="card-title mb-3"),
                *[
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Span(nome, className="fw-semibold"),
                                    html.Span(f"{pct}%", className="float-end text-muted small"),
                                ],
                                className="mb-1",
                            ),
                            dbc.Progress(value=pct, color="primary", className="mb-3"),
                        ]
                    )
                    for nome, pct in itens
                ],
            ]
        ),
        className="shadow-sm h-100",
    )

layout = dbc.Container(
    [
        html.H2("Skills", className="mb-1 fw-bold"),
        html.P("Principais competências técnicas e comportamentais", className="text-muted mb-4"),
        dbc.Row(
            [
                dbc.Col(skill_group(titulo, itens), md=4, className="mb-3")
                for titulo, itens in SKILLS.items()
            ]
        ),
    ],
    className="py-3",
)