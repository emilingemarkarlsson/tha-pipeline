from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Generate fake data for Team Key Stats
def get_kpi_data():
    return pd.DataFrame({
        "KPI": [
            "Win?", "Goals", "Goals Against", "% Shots on Goal",
            "Puck Battles Won, %", "Accurate Passes, %", "Faceoffs Won, %",
            "Power Play, %", "Short-Handed, %"
        ],
        "Current Value": [1, 5, 3, 75, 60, 85, 48, 25, 15],  # Replace with realistic values
        "Target Value": [1, 6, 2, 80, 65, 90, 55, 30, 20],  # Replace with realistic targets
        "Progress (%)": [100, 83.3, 150, 93.8, 92.3, 94.4, 87.3, 83.3, 75],  # Progress based on current/target
    })

# Generate fake data for trends over games
def get_trend_data():
    games = [f"Game {i}" for i in range(1, 11)]
    return pd.DataFrame({
        "Game": games,
        "Goals": [1, 2, 3, 2, 4, 5, 3, 4, 2, 6],
        "Goals Against": [3, 2, 1, 3, 2, 1, 3, 2, 1, 2],
        "% Shots on Goal": [60, 65, 70, 68, 72, 75, 78, 80, 82, 85],
        "Puck Battles Won, %": [50, 55, 60, 58, 62, 65, 67, 70, 72, 75],
        "Accurate Passes, %": [78, 80, 82, 81, 83, 85, 86, 88, 89, 90],
        "Faceoffs Won, %": [48, 50, 52, 54, 55, 57, 58, 60, 62, 65],
        "Power Play, %": [18, 20, 22, 25, 26, 28, 30, 32, 34, 35],
        "Short-Handed, %": [10, 12, 14, 15, 16, 18, 20, 22, 23, 25],
    })

# Create KPI Table with Progress Bars
def kpi_table(kpi_data):
    rows = []
    for _, row in kpi_data.iterrows():
        color = "success" if row["Progress (%)"] >= 80 else "warning" if row["Progress (%)"] >= 50 else "danger"
        rows.append(
            dbc.Row(
                [
                    dbc.Col(html.Div(row["KPI"], style={"font-weight": "bold", "text-align": "center"}), width=2),
                    dbc.Col(html.Div(f"{row['Current Value']} / {row['Target Value']}", style={"text-align": "center"}), width=2),
                    dbc.Col(
                        dbc.Progress(
                            value=min(row["Progress (%)"], 100),
                            color=color,
                            striped=True,
                            animated=True,
                            style={"height": "15px"}
                        ),
                        width=6
                    ),
                    dbc.Col(html.Div(f"{row['Progress (%)']:.2f}%", style={"text-align": "center", "color": color, "font-weight": "bold"}), width=2),
                ],
                style={"margin-bottom": "10px"}
            )
        )
    return html.Div(rows, style={"margin-top": "20px"})

# Create trend graphs for each KPI
def trend_graphs(trend_data):
    graphs = []
    for column in trend_data.columns[1:]:
        fig = px.line(
            trend_data,
            x="Game",
            y=column,
            title=f"{column} Over Games",
            markers=True,
            line_shape="spline",
            labels={column: column, "Game": "Game"}
        )
        fig.update_traces(line_color="#233762")
        fig.update_layout(margin={"l": 10, "r": 10, "t": 40, "b": 40})
        graphs.append(dcc.Graph(figure=fig, style={"height": "300px"}))
    return graphs

# Main Layout
def layout(conn=None):
    kpi_data = get_kpi_data()
    trend_data = get_trend_data()

    kpi_section = kpi_table(kpi_data)
    trend_section = trend_graphs(trend_data)

    return dbc.Container(
        [
            html.H2("Team Key Stats", className="content-title"),
            html.Hr(),
            html.Div(kpi_section),
            html.Br(),
            html.H4("KPI Trends Over Games"),
            dbc.Row([dbc.Col(graph, width=6) for graph in trend_section]),
        ],
        fluid=True,  # Ensures proper alignment with the sidebar
        style={"padding": "20px"}  # Adds padding for spacing
    )