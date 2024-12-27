import sys
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="dash_auth")

# Add the root directory (tha-pipeline) to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dashboard.auth import add_authentication  # Import the authentication utility
from dashboard.db_utils import get_connection  # Import the database connection utility

# Import page layouts
from pages.organization_stats import layout as organization_stats_layout

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
    id="sidebar",  # Add ID for callback targeting
    children=[
        html.Div(
            html.Img(
                src="/assets/img/SonderjyskE_logo.svg.png",
                className="logo"
            ),
            className="sidebar-logo-container"
        ),
        html.H5("Key Stats", className="menu-category"),  # Category Header
        dbc.Nav(
            [
                dbc.NavLink("Organization Stats", href="/organization-stats", active="exact"),
                dbc.NavLink("Team Stats", href="/team-stats", active="exact"),
                dbc.NavLink("Player Stats", href="/player-stats", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),

        html.H5("Trends", className="menu-category"),  # Category Header
        dbc.Nav(
            [
                dbc.NavLink("Season Trends", href="/season-trends", active="exact"),
                dbc.NavLink("Player Trends", href="/player-trends", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),

        html.H5("Comparisons", className="menu-category"),  # Category Header
        dbc.Nav(
            [
                dbc.NavLink("Team Comparisons", href="/team-comparisons", active="exact"),
                dbc.NavLink("Player Comparisons", href="/player-comparisons", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)

# Sidebar Toggle Button (Visible on Mobile)
sidebar_toggle = dbc.Button(
    "☰", id="sidebar-toggle", outline=True, color="primary", className="d-md-none"
)

# Top Navbar
top_navbar = dbc.Navbar(
    dbc.Container(
        [
            sidebar_toggle,
            html.Div("Version 0.1", className="navbar-title"),
        ],
        fluid=True,
    ),
    style={"background-color": "#F6F7F9"},  # Light background color
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

# Callback to toggle the sidebar on mobile
@app.callback(
    Output("sidebar", "style"),  # Toggles sidebar visibility
    [Input("sidebar-toggle", "n_clicks")],
    prevent_initial_call=True
)
def toggle_sidebar(n_clicks):
    if n_clicks and n_clicks % 2 == 1:  # Show sidebar on odd clicks
        return {"display": "block"}  # Show the sidebar
    else:  # Hide sidebar on even clicks
        return {"display": "none"}  # Hide the sidebar

# Callback for dynamic page rendering
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    # Connect to DuckDB for dynamic data fetching
    conn = get_connection()

    if pathname == "/organization-stats":
        # Pass the connection object to the organization_stats layout
        return organization_stats_layout(conn)
    else:
        return html.H1("Welcome to the Hockey Analytics Dashboard!", className="content-title")

# Run the server
if __name__ == "__main__":
    # Ensure the app listens on all network interfaces and the correct port for Docker
    app.run_server(host="0.0.0.0", port=8050, debug=True)