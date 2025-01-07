from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

# Dummy Data for Visualization
import pandas as pd
import numpy as np

# Dummy data for example purposes
def get_team_data():
    games = [f"Game {i}" for i in range(1, 21)]
    return pd.DataFrame({
        "game": games,
        "shots": np.random.randint(20, 50, len(games)),
        "puck_battles_won": np.random.randint(10, 30, len(games)),
        "attacks_typology": np.random.randint(5, 15, len(games)),
        "takeaways": np.random.randint(5, 20, len(games)),
        "puck_losses": np.random.randint(5, 20, len(games)),
        "playtime_phases": np.random.randint(10, 40, len(games)),
        "power_play_efficiency": np.random.uniform(10, 50, len(games)),
        "short_handed_efficiency": np.random.uniform(5, 25, len(games)),
        "passes": np.random.randint(50, 150, len(games)),
        "entries": np.random.randint(10, 50, len(games)),
        "breakouts": np.random.randint(10, 30, len(games)),
        "faceoffs_won": np.random.randint(5, 15, len(games)),
    })

# Layout for the Overview Tab
def overview_tab(data):
    total_shots = data["shots"].sum()
    total_puck_battles = data["puck_battles_won"].sum()
    total_takeaways = data["takeaways"].sum()
    total_entries = data["entries"].sum()

    # KPI Cards
    kpi_cards = dbc.Row(
        [
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Total Shots", className="card-title"),
                    html.H2(f"{total_shots}", className="card-text"),
                ])
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Puck Battles Won", className="card-title"),
                    html.H2(f"{total_puck_battles}", className="card-text"),
                ])
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Total Takeaways", className="card-title"),
                    html.H2(f"{total_takeaways}", className="card-text"),
                ])
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Total Entries", className="card-title"),
                    html.H2(f"{total_entries}", className="card-text"),
                ])
            ]), width=3),
        ]
    )

    # Bar Chart: Shots vs Puck Battles
    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(
        x=data["game"],
        y=data["shots"],
        name="Shots",
        marker_color="#5EC577",
    ))
    bar_fig.add_trace(go.Bar(
        x=data["game"],
        y=data["puck_battles_won"],
        name="Puck Battles Won",
        marker_color="#233762",
    ))
    bar_fig.update_layout(
        title="Shots vs Puck Battles by Game",
        barmode="group",
        xaxis_title="Game",
        yaxis_title="Count",
        height=400,
    )

    # Line Chart: Takeaways and Entries
    line_fig = px.line(
        data,
        x="game",
        y=["takeaways", "entries"],
        title="Takeaways and Entries by Game",
        markers=True,
        labels={"value": "Count", "variable": "Metric"},
    )
    line_fig.update_traces(line_color="#233762")

    return html.Div([
        html.H2("Overview", className="content-title"),
        kpi_cards,
        html.Br(),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=bar_fig), width=6),
            dbc.Col(dcc.Graph(figure=line_fig), width=6),
        ]),
    ])

# Layout for the Shots Tab
def shots_tab(data):
    shots_fig = px.bar(
        data,
        x="game",
        y="shots",
        title="Shots Per Game",
        labels={"shots": "Shots", "game": "Game"},
        color="shots",
        color_continuous_scale="Viridis",
    )
    return html.Div([
        html.H2("Shots Metrics", className="content-title"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=shots_fig), width=12),
        ]),
    ])

# Layout for the Puck Battles Tab
def puck_battles_tab(data):
    battles_fig = px.bar(
        data,
        x="game",
        y="puck_battles_won",
        title="Puck Battles Won Per Game",
        labels={"puck_battles_won": "Puck Battles Won", "game": "Game"},
        color="puck_battles_won",
        color_continuous_scale="Blues",
    )
    return html.Div([
        html.H2("Puck Battles Metrics", className="content-title"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=battles_fig), width=12),
        ]),
    ])

# Additional Tabs with Similar Structures
def attacks_typology_tab(data):
    return html.Div([
        html.H2("Attacks Typology Metrics", className="content-title"),
        dbc.Row([
            dbc.Col(dcc.Graph(
                figure=px.bar(data, x="game", y="attacks_typology", title="Attacks Typology Per Game")
            ), width=12),
        ]),
    ])

def takeaways_tab(data):
    return html.Div([
        html.H2("Takeaways Metrics", className="content-title"),
        dbc.Row([
            dbc.Col(dcc.Graph(
                figure=px.line(data, x="game", y="takeaways", title="Takeaways Per Game")
            ), width=12),
        ]),
    ])

def puck_losses_tab(data):
    return html.Div([
        html.H2("Puck Losses Metrics", className="content-title"),
        dbc.Row([
            dbc.Col(dcc.Graph(
                figure=px.bar(data, x="game", y="puck_losses", title="Puck Losses Per Game")
            ), width=12),
        ]),
    ])

def playtime_phases_tab(data):
    return html.Div([
        html.H2("Playtime Phases Metrics", className="content-title"),
        dbc.Row([
            dbc.Col(dcc.Graph(
                figure=px.bar(data, x="game", y="playtime_phases", title="Playtime Phases Per Game")
            ), width=12),
        ]),
    ])

# Main Layout Function
def layout(conn=None):
    # Load data (replace with actual database query)
    data = get_team_data()

    # Tabs
    tabs = dbc.Tabs(
        [
            dbc.Tab(overview_tab(data), label="Overview"),
            dbc.Tab(shots_tab(data), label="Shots"),
            dbc.Tab(puck_battles_tab(data), label="Puck Battles"),
            dbc.Tab(attacks_typology_tab(data), label="Attacks Typology"),
            dbc.Tab(takeaways_tab(data), label="Takeaways"),
            dbc.Tab(puck_losses_tab(data), label="Puck Losses"),
            dbc.Tab(playtime_phases_tab(data), label="Playtime Phases"),
        ]
    )

    return html.Div([
        tabs
    ])