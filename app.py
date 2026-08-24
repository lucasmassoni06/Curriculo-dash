import dash
import dash_bootstrap_components as dbc
from dash import html

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.CYBORG, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
)
server = app.server
app.title = "Portfólio | Currículo Interativo"

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("Meu Portfólio", href="/", className="fw-bold"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Home", href="/", active="exact")),
                    dbc.NavItem(dbc.NavLink("Qualificações", href="/qualificacoes", active="exact")),
                    dbc.NavItem(dbc.NavLink("Skills", href="/skills", active="exact")),
                    dbc.NavItem(dbc.NavLink("Análise de Dados", href="/analise", active="exact")),
                ],
                pills=True,
            ),
        ],
        fluid=True,
    ),
    color="dark",
    dark=True,
    className="mb-4 sticky-top",
)

app.layout = dbc.Container(
    [
        navbar,
        dash.page_container,
        html.Hr(className="my-5"),
        html.Footer(
            "Feito com Plotly Dash",
            className="text-center text-muted small pb-3",
        ),
    ],
    fluid=True,
    className="px-4",
)

server = app.server

if __name__ == "__main__":
    app.run(debug=True)