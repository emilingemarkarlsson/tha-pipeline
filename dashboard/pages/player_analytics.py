import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from dashboard.utils.db_utils import get_connection

def get_player_data(conn):
    # First check available columns
    try:
        columns = conn.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'main' 
            AND table_name = 'dk_metal_league_ep'
            ORDER BY ordinal_position;
        """).fetchall()
        print("Available columns:", [col[0] for col in columns])
        
        # Query with correct column names
        result = conn.execute("""
            SELECT 
                "teamName",
                "team/name" as team_name,
                "stats/games" as games,
                "stats/points" as points
            FROM dk_metal_league_ep 
            WHERE "teamName" = 'SønderjyskE'
            LIMIT 10;
        """).fetchall()
        
        return pd.DataFrame(result, columns=['team_name', 'games', 'points'])
    except Exception as e:
        print(f"Query error: {e}")
        return pd.DataFrame(columns=['team_name', 'games', 'points'])

def layout(conn=None):
    df = get_player_data(conn) if conn else pd.DataFrame()
    
    return html.Div([
        html.H1("Player Trends"),
        dbc.Tabs([
            dbc.Tab(label="Performance Over Time", children=[
                html.Div([
                    html.H3("Player Statistics"),
                    dcc.Graph(
                        figure={
                            'data': [
                                {'x': df['team_name'], 'y': df['points'], 'type': 'bar', 'name': 'Points'}
                            ],
                            'layout': {
                                'title': 'Player Points'
                            }
                        }
                    )
                ])
            ], tab_id="tab-0"),
            dbc.Tab(label="Seasonal Analysis", children=[
                html.P("Season-by-season analysis will be shown here")
            ], tab_id="tab-1"),
            dbc.Tab(label="Historical Stats", children=[
                html.P("Historical statistics will be shown here")
            ], tab_id="tab-2")
        ], active_tab="tab-0")
    ])