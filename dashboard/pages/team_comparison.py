import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Function to generate demo data for SønderjyskE trends
def get_demo_sonderjyske_trends():
    return pd.DataFrame({
        "season": ["2018-2019", "2019-2020", "2020-2021", "2021-2022", "2022-2023"],
        "total_points": [80, 85, 78, 90, 88],
        "goals_for": [150, 160, 140, 170, 165],
        "goals_against": [120, 115, 125, 110, 130],
        "games_played": [50, 48, 52, 50, 54]
    })

# Function to generate demo league data
def get_demo_league_data():
    return pd.DataFrame({
        "team": ["SønderjyskE", "Rungsted", "Aalborg", "Herning"],
        "season": ["2022-2023", "2022-2023", "2022-2023", "2022-2023"],
        "games_played": [54, 54, 54, 54],
        "total_points": [88, 85, 82, 80],
        "goals_for": [165, 160, 155, 150],
        "goals_against": [130, 135, 140, 145],
        "goal_difference": [35, 25, 15, 5]
    })

# Page layout function with demo data
def layout(conn=None):
    # Generate demo data
    sonderjyske_data = get_demo_sonderjyske_trends()
    league_data = get_demo_league_data()

    # Calculate additional metrics for SønderjyskE
    sonderjyske_data["points_per_game"] = sonderjyske_data["total_points"] / sonderjyske_data["games_played"]

    # Section 1: SønderjyskE Trends
    sonderjyske_points_per_game_fig = px.area(
        sonderjyske_data, 
        x="season", 
        y="points_per_game",
        title="SønderjyskE: Average Points Per Game Over Seasons",
        labels={"points_per_game": "Points Per Game", "season": "Season"},
        markers=True
    )

    sonderjyske_goals_fig = px.line(
        sonderjyske_data, 
        x="season", 
        y="goals_for",
        title="SønderjyskE: Goals Scored Over Seasons",
        labels={"goals_for": "Goals Scored", "season": "Season"},
        markers=True
    )

    sonderjyske_goals_against_fig = px.line(
        sonderjyske_data, 
        x="season", 
        y="goals_against",
        title="SønderjyskE: Goals Conceded Over Seasons",
        labels={"goals_against": "Goals Conceded", "season": "Season"},
        markers=True
    )

    # Section 2: General League Stats
    points_per_team_fig = px.bar(
        league_data, 
        x="team", 
        y="total_points", 
        color="total_points",
        title="Total Points per Team",
        labels={"team": "Team", "total_points": "Total Points"}
    )

    goals_fig = px.scatter(
        league_data, 
        x="goals_for", 
        y="goals_against", 
        color="team", 
        size="goal_difference",
        title="Goals For vs. Goals Against by Team",
        labels={"goals_for": "Goals For", "goals_against": "Goals Against", "team": "Team"}
    )

    # Section 3: Team Comparison
    comparison_goals_fig = px.bar(
        league_data, 
        x="team", 
        y="goals_for", 
        title="Team Comparison: Goals Scored",
        labels={"team": "Team", "goals_for": "Goals Scored"}
    )

    comparison_points_fig = px.bar(
        league_data, 
        x="team", 
        y="total_points", 
        title="Team Comparison: Total Points",
        labels={"team": "Team", "total_points": "Total Points"}
    )

    # Page Layout
    return html.Div(
        [
            # Section 1: SønderjyskE Trends
            html.H2("SønderjyskE Team Trends", className="content-title"),
            html.Hr(),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=sonderjyske_points_per_game_fig), width=4),
                dbc.Col(dcc.Graph(figure=sonderjyske_goals_fig), width=4),
                dbc.Col(dcc.Graph(figure=sonderjyske_goals_against_fig), width=4),
            ]),
            html.Br(),

            # Section 2: General League Stats
            html.H2("League EP Stats", className="content-title"),
            html.Hr(),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=points_per_team_fig), width=6),
                dbc.Col(dcc.Graph(figure=goals_fig), width=6),
            ]),
            html.Br(),

            # Section 3: Team Comparison
            html.H2("Team Comparison", className="content-title"),
            html.Hr(),
            dbc.Tabs([
                dbc.Tab(label="Head to Head", children=[
                    dbc.Row([
                        dbc.Col(dcc.Graph(figure=comparison_goals_fig), width=6),
                        dbc.Col(dcc.Graph(figure=comparison_points_fig), width=6)
                    ])
                ], tab_id="tab-0"),
                dbc.Tab(label="League Overview", children=[
                    html.P("League overview comparison will be shown here.")
                ], tab_id="tab-1")
            ], active_tab="tab-0")
        ],
        className="content scrollable-content"
    )