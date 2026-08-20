import dash
import dash_bootstrap_components as dbc
from dash import html
from dados import PESSOA

dash.register_page(__name__, path="/", name="Home", title="Home")

def case_card(case):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(case["titulo"], className="card-title"),
                html.P(case["resumo"], className="card-text text-secondary"),
                html.Span(case["resultado"], className="badge text-bg-success"),
            ]
        ),
        className="mb-3 h-100 shadow-sm",
    )

def formacao_item(f):
    return dbc.ListGroupItem(
        [
            html.Div(f["curso"], className="fw-semibold"),
            html.Small(f"{f['instituicao']} • {f['ano']}", className="text-muted"),
        ]
    )

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Img(
                        src="/assets/foto.jpg",
                        className="img-fluid rounded-circle shadow",
                        style={"max-width": "180px"},
                    ),
                    md=3,
                    className="text-center",
                ),
                dbc.Col(
                    [
                        html.H1(PESSOA["nome"], className="display-5 fw-bold"),
                        html.H4(PESSOA["cargo"], className="text-primary"),
                        html.P(
                            [html.I(className="bi bi-geo-alt me-1"), PESSOA["cidade"]],
                            className="text-muted mb-1",
                        ),
                        html.P(
                            [
                                html.I(className="bi bi-envelope me-1"),
                                html.A(PESSOA["email"], href=f"mailto:{PESSOA['email']}", className="me-3"),
                                html.I(className="bi bi-linkedin me-1"),
                                html.A("LinkedIn", href=f"https://{PESSOA['linkedin']}", target="_blank"),
                            ],
                            className="text-muted",
                        ),
                    ],
                    md=9,
                    className="d-flex flex-column justify-content-center",
                ),
            ],
            className="mb-5 align-items-center",
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("Quem sou eu", className="card-title"),
                            html.P(PESSOA["minibio"], className="card-text"),
                        ]
                    ),
                    className="shadow-sm",
                )
            )
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.H5("Formação", className="mt-4 mb-2 fw-bold"),
                    dbc.ListGroup([formacao_item(f) for f in PESSOA["formacao"]], flush=True),
                ]
            )
        ),
        html.H5("Casos reais", className="mt-4 mb-2 fw-bold"),
        dbc.Row([dbc.Col(case_card(c), md=6) for c in PESSOA["cases"]]),
    ],
    className="py-3",
)