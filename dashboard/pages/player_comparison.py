import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dashboard.utils.db_utils import get_connection

def layout(conn=None):
    return html.Div([
        html.H1("Player Comparison"),
        dbc.Tabs([
            dbc.Tab(label="Head to Head", children=[
                html.P("Player head to head comparison will be shown here")
            ], tab_id="tab-0"),
            dbc.Tab(label="Statistical Comparison", children=[
                html.P("Detailed statistical comparison will be shown here")
            ], tab_id="tab-1"),
            dbc.Tab(label="Historical Matchups", children=[
                html.P("Historical matchup data will be shown here")
            ], tab_id="tab-2")
        ], active_tab="tab-0")
    ])