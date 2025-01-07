import sys
import os
from pathlib import Path
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="dash_auth")

# Add the root directory (tha-pipeline) to the Python module search path
root_dir = Path(__file__).resolve().parent.parent  # Parent directory of 'dashboard'
sys.path.append(str(root_dir))  # Add 'tha-pipeline' to sys.path

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dashboard.auth import add_authentication  # Authentication utility
from dashboard.utils.db_utils import get_connection  # Database connection utility

# Import layouts for each page
from dashboard.pages.team_keystats import layout as team_keystats_layout
from dashboard.pages.player_keystats import layout as player_keystats_layout
from dashboard.pages.team_analytics import layout as team_trend_layout
from dashboard.pages.player_analytics import layout as player_trend_layout
from dashboard.pages.predictions_ai import layout as predictions_ai_layout
from dashboard.pages.feedback import layout as feedback_layout  # Feedback page layout

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,  # Required for dynamic callbacks
)
app.title = "Hockey Analytics Dashboard"

# Add authentication to the app
add_authentication(app)

# Sidebar with Links
sidebar = html.Div(
    id="sidebar",
    children=[
        html.H5("Key Stats", className="menu-category"),
        dbc.Nav(
            [
                dbc.NavLink("Team Key Stats", href="/team-keystats", active="exact"),
                dbc.NavLink("Player Key Stats", href="/player-keystats", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),

        html.H5("Trend Analytics", className="menu-category"),
        dbc.Nav(
            [
                dbc.NavLink("Team Trends", href="/team-trends", active="exact"),
                dbc.NavLink("Player Trends", href="/player-trends", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),

        html.H5("AI Prediction", className="menu-category"),
        dbc.Nav(
            [
                html.Div([
                    dbc.NavLink("Predictions", href="/predictions-ai", active="exact"),
                    html.Span(
                        "BETA",
                        style={
                            "background-color": "#ffd700",
                            "color": "#000",
                            "padding": "2px 6px",
                            "border-radius": "4px",
                            "font-size": "10px",
                            "margin-left": "8px",
                            "font-weight": "bold"
                        }
                    )
                ], style={"display": "flex", "align-items": "center"}),
            ],
            vertical=True,
            pills=True,
        ),

        # Add Feedback Text Link at the bottom
        html.Div(
            dbc.NavLink(
                "Feedback",
                href="/feedback",
                active="exact",
                className="feedback-link"
            ),
            style={"margin-top": "auto"}  # Push Feedback link to the bottom of the sidebar
        ),
    ],
    className="sidebar",
    style={
        "position": "relative",
        "height": "100%",
        "display": "flex",
        "flex-direction": "column"  # Ensures the sidebar uses all vertical space
    },
)

# Top Navbar
top_navbar = dbc.Navbar(
    dbc.Container(
        [
            html.Div(
                [
                    html.Img(
                        src="/assets/img/SonderjyskE_logo.svg.png",
                        style={"height": "30px", "margin-right": "10px"}
                    ),
                    html.Span(
                        "Sonderjyske",
                        style={
                            "font-weight": "bold", 
                            "font-size": "18px", 
                            "color": "#343a40"
                        }
                    ),
                ],
                style={"display": "flex", "align-items": "center"}
            ),
        ],
        fluid=True,
    ),
    style={"background-color": "#F6F7F9", "padding": "10px 15px"},
    dark=False,
    sticky="top",
    className="top-navbar",
)

# Layout for the Main App
app.layout = html.Div(
    [
        dcc.Location(id="url"),  # Tracks the current page URL
        top_navbar,
        html.Div(
            [sidebar, html.Div(id="page-content", className="content scrollable-content")],
            className="main-layout"
        ),
    ]
)

# Callback for dynamic page rendering
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    conn = get_connection()
    
    # Define routes with their corresponding layouts
    routes = {
        "/": team_keystats_layout(conn),  # Default to Team Key Stats
        "/team-keystats": team_keystats_layout(conn),
        "/player-keystats": player_keystats_layout(conn),
        "/team-trends": team_trend_layout(conn),
        "/player-trends": player_trend_layout(conn),
        "/predictions-ai": predictions_ai_layout(conn),
        "/feedback": feedback_layout(conn),  # Feedback page route
    }
    
    # Return the layout for the current route or default to team key stats
    return routes.get(pathname, team_keystats_layout(conn))

# Add URL redirect callback
@app.callback(
    Output("url", "pathname"),
    Input("url", "pathname")
)
def redirect_to_default(pathname):
    if not pathname or pathname == "/":
        return "/team-keystats"  # Default to Team Key Stats
    return pathname

# Run the server
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)