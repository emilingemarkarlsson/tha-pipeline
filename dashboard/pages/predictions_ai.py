from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Generate dummy data for AI predictions
def get_ai_player_data():
    players = [f"Player {i}" for i in range(1, 26)]
    return pd.DataFrame({
        "Player": players,
        "Performance Score": np.random.randint(50, 100, len(players)),
        "Fatigue Index (%)": np.random.uniform(10, 40, len(players)),
        "Optimal Playtime (min)": np.random.randint(10, 30, len(players)),
        "Potential Goals (Season)": np.random.randint(10, 40, len(players)),
    })

def get_ai_team_data():
    games = [f"Game {i}" for i in range(1, 21)]
    return pd.DataFrame({
        "Game": games,
        "Tactic Effectiveness (%)": np.random.uniform(70, 100, len(games)),
        "Defensive Strength (%)": np.random.uniform(50, 90, len(games)),
        "Predicted Win Probability (%)": np.random.uniform(50, 95, len(games)),
        "Power Play Success (%)": np.random.uniform(10, 50, len(games)),
    })

def get_game_strategy_data():
    strategies = ["Offensive Play", "Defensive Play", "Special Teams Play"]
    return pd.DataFrame({
        "Strategy": strategies,
        "Projected Success Rate (%)": np.random.uniform(60, 95, len(strategies)),
        "Recommended Focus (%)": np.random.uniform(30, 60, len(strategies)),
    })

# Layout for Team Performance Tab
def team_performance_tab(team_data):
    tactic_fig = px.line(
        team_data,
        x="Game",
        y="Tactic Effectiveness (%)",
        title="Tactic Effectiveness Over Games",
        markers=True,
        line_shape="spline",
    )
    tactic_fig.update_traces(line_color="#233762")
    
    defensive_fig = px.line(
        team_data,
        x="Game",
        y="Defensive Strength (%)",
        title="Defensive Strength Over Games",
        markers=True,
        line_shape="spline",
        color_discrete_sequence=["#5EC577"],
    )

    win_probability_fig = px.bar(
        team_data,
        x="Game",
        y="Predicted Win Probability (%)",
        title="Predicted Win Probability",
        labels={"Predicted Win Probability (%)": "Win Probability (%)"},
        color="Predicted Win Probability (%)",
        color_continuous_scale="Viridis",
    )

    return html.Div([
        html.H2("Team Performance", className="content-title"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=tactic_fig), width=6),
            dbc.Col(dcc.Graph(figure=defensive_fig), width=6),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=win_probability_fig), width=12),
        ]),
    ])

# Layout for Player Performance Tab
def player_performance_tab(player_data):
    performance_fig = px.bar(
        player_data,
        x="Player",
        y="Performance Score",
        title="Player Performance Scores",
        labels={"Performance Score": "Performance Score"},
        color="Performance Score",
        color_continuous_scale="Blues",
    )

    fatigue_fig = px.scatter(
        player_data,
        x="Optimal Playtime (min)",
        y="Fatigue Index (%)",
        size="Potential Goals (Season)",
        color="Fatigue Index (%)",
        title="Optimal Playtime vs Fatigue",
        labels={"Fatigue Index (%)": "Fatigue Index (%)", "Optimal Playtime (min)": "Optimal Playtime (min)"},
        hover_data=["Player"],
        color_continuous_scale="reds",
    )

    return html.Div([
        html.H2("Player Performance", className="content-title"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=performance_fig), width=6),
            dbc.Col(dcc.Graph(figure=fatigue_fig), width=6),
        ]),
    ])

# Layout for Game Strategy Tab
def game_strategy_tab(strategy_data):
    radar_fig = go.Figure()

    for _, row in strategy_data.iterrows():
        radar_fig.add_trace(go.Scatterpolar(
            r=[row["Projected Success Rate (%)"], row["Recommended Focus (%)"], 100],
            theta=["Projected Success Rate", "Recommended Focus", "Max Potential"],
            fill="toself",
            name=row["Strategy"],
        ))

    radar_fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        title="Game Strategy Success Potential",
    )

    strategy_focus_fig = px.bar(
        strategy_data,
        x="Strategy",
        y="Recommended Focus (%)",
        title="Recommended Strategy Focus",
        labels={"Recommended Focus (%)": "Focus (%)"},
        color="Recommended Focus (%)",
        color_continuous_scale="greens",
    )

    return html.Div([
        html.H2("Game Strategy", className="content-title"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=radar_fig), width=6),
            dbc.Col(dcc.Graph(figure=strategy_focus_fig), width=6),
        ]),
    ])

# Layout for AI Predictions Overview
def overview_tab(player_data, team_data):
    # KPI Cards
    kpi_cards = dbc.Row(
        [
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Average Team Tactic Effectiveness", className="card-title"),
                    html.H2(f"{team_data['Tactic Effectiveness (%)'].mean():.1f}%", className="card-text"),
                ])
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Top Player Performance Score", className="card-title"),
                    html.H2(f"{player_data['Performance Score'].max():.1f}", className="card-text"),
                ])
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Average Predicted Win Rate", className="card-title"),
                    html.H2(f"{team_data['Predicted Win Probability (%)'].mean():.1f}%", className="card-text"),
                ])
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Optimal Playtime (min)", className="card-title"),
                    html.H2(f"{player_data['Optimal Playtime (min)'].mean():.1f}", className="card-text"),
                ])
            ]), width=3),
        ]
    )

    return html.Div([
        html.H2("AI-Powered Insights", className="content-title"),
        kpi_cards,
    ])

# Main Layout Function
def layout(conn=None):
    player_data = get_ai_player_data()
    team_data = get_ai_team_data()
    strategy_data = get_game_strategy_data()

    tabs = dbc.Tabs(
        [
            dbc.Tab(overview_tab(player_data, team_data), label="Overview"),
            dbc.Tab(team_performance_tab(team_data), label="Team Performance"),
            dbc.Tab(player_performance_tab(player_data), label="Player Performance"),
            dbc.Tab(game_strategy_tab(strategy_data), label="Game Strategy"),
        ]
    )

    return html.Div([
        tabs
    ])