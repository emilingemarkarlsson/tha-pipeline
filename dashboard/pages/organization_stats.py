from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from dashboard.db_utils import get_connection

# Function to fetch data for SønderjyskE trends
def fetch_sonderjyske_trends(conn):
    query = """
        SELECT 
            year AS Season, 
            totalpoints AS Total_Points, 
            goalsfore AS Goals_For, 
            goalsagainst AS Goals_Against, 
            gp AS Games_Played
        FROM dk_metal_league_ep
        WHERE team = 'SønderjyskE'
    """
    return conn.execute(query).df()

# Function to fetch general league data
def fetch_dk_metal_league_ep_data(conn):
    query = """
        SELECT 
            team, 
            year AS Season, 
            rank, 
            gp AS Games_Played, 
            wins AS Wins, 
            losses AS Losses, 
            goalsfore AS Goals_For, 
            goalsagainst AS Goals_Against, 
            goaldifference AS Goal_Difference, 
            totalpoints AS Total_Points
        FROM dk_metal_league_ep
    """
    return conn.execute(query).df()

# Page layout function to dynamically load data
def layout(conn):
    # Fetch data
    sonderjyske_data = fetch_sonderjyske_trends(conn)
    league_ep_data = fetch_dk_metal_league_ep_data(conn)

    # Calculate Points Per Game for SønderjyskE
    sonderjyske_data["Points_Per_Game"] = sonderjyske_data["Total_Points"] / sonderjyske_data["Games_Played"]

    # Section 1: SønderjyskE Trends
    sonderjyske_points_per_game_fig = px.bar(
        sonderjyske_data, 
        x="Season", 
        y="Points_Per_Game",
        title="SønderjyskE: Average Points Per Game Per Season",
        labels={"Points_Per_Game": "Points Per Game", "Season": "Season"},
        color="Points_Per_Game",  # Color bars by their height
        text="Points_Per_Game"  # Display the value on the bar
    )

    # Update styling to match the desired style
    sonderjyske_points_per_game_fig.update_traces(
        texttemplate='%{text:.1f}',  # One decimal point
        textposition='outside'  # Place text above bars
    )
    sonderjyske_points_per_game_fig.update_xaxes(
        tickmode='linear',  # Ensure every year is displayed
        dtick=1,            # Interval of 1 year
        tickangle=-45       # Rotate x-axis labels diagonally
    )
    sonderjyske_points_per_game_fig.update_layout(
        xaxis=dict(
            title=None,  # Remove x-axis title
        ),
        yaxis=dict(
            title="Points Per Game",
            gridcolor="rgba(200, 200, 200, 0.3)"  # Light gridlines
        ),
        plot_bgcolor="rgba(0, 0, 0, 0)",  # Transparent background
        paper_bgcolor="#1f1f1f",  # Dark grey background for the figure
        font=dict(
            color="white",  # White font for text
            size=14         # Adjust font size
        ),
        title=dict(
            font=dict(size=16),  # Larger title font
            x=0.5  # Center the title
        )
    )
    sonderjyske_points_per_game_fig.update_traces(
        marker=dict(color="#1f77b4")  # Set bar color to blue
    )

    sonderjyske_goals_fig = px.line(
        sonderjyske_data, x="Season", y="Goals_For",
        title="SønderjyskE: Goals Scored Over Seasons",
        labels={"Goals_For": "Goals Scored", "Season": "Season"},
        markers=True  # Add markers for round points
    )

    sonderjyske_goals_against_fig = px.line(
        sonderjyske_data, x="Season", y="Goals_Against",
        title="SønderjyskE: Goals Conceded Over Seasons",
        labels={"Goals_Against": "Goals Conceded", "Season": "Season"},
        markers=True  # Add markers for round points
    )

    # Section 2: General League Stats
    # Handle invalid values for size (negative Goal_Difference)
    league_ep_data["Bubble_Size"] = league_ep_data["Goal_Difference"].apply(lambda x: abs(x) if x > 0 else 1)

    points_per_team_fig = px.bar(
        league_ep_data, x="team", y="Total_Points", color="Total_Points",
        title="Total Points per Team",
        labels={"team": "Team", "Total_Points": "Total Points"},
        hover_data=["Season", "Games_Played", "Wins", "Losses"]
    )

    goals_fig = px.scatter(
        league_ep_data, x="Goals_For", y="Goals_Against", color="team", size="Bubble_Size",
        title="Goals For vs. Goals Against by Team",
        labels={"Goals_For": "Goals For", "Goals_Against": "Goals Against", "team": "Team"},
        hover_data=["Season", "Goal_Difference"]
    )

    # Page Layout
    return html.Div(
        [
            # Section 1: SønderjyskE Trends
            html.H2("SønderjyskE Team Trends", className="content-title"),
            html.Hr(),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=sonderjyske_points_per_game_fig, className="graph-block"), width=4),
                dbc.Col(dcc.Graph(figure=sonderjyske_goals_fig, className="graph-block"), width=4),
                dbc.Col(dcc.Graph(figure=sonderjyske_goals_against_fig, className="graph-block"), width=4),
            ]),

            # Section 2: General League Stats
            html.H2("League EP Stats", className="content-title"),
            html.Hr(),
            html.H4("Team Performance Metrics"),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=points_per_team_fig, className="graph-block"), width=6),
                dbc.Col(dcc.Graph(figure=goals_fig, className="graph-block"), width=6),
            ]),
        ],
        className="content scrollable-content"
    )