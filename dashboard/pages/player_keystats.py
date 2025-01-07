from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px

# Generate fake data for Player Key Stats by category
def get_player_kpi_data():
    players = {
        "Goalkeepers": ["Player 1", "Player 2"],
        "Defenders": [f"Player {i}" for i in range(3, 11)],  # Players 3-10
        "Centers": [f"Player {i}" for i in range(11, 15)],  # Players 11-14
        "Forwards": [f"Player {i}" for i in range(15, 24)]  # Players 15-23
    }
    kpi_data = {}
    for category, player_list in players.items():
        kpi_data[category] = pd.DataFrame({
            "Player": player_list,
            "Goals" if category != "Goalkeepers" else "Saves": [round(x, 1) for x in (20 * np.random.rand(len(player_list)))],
            "Goals Against" if category != "Goalkeepers" else "Save %": [round(x, 1) for x in (15 * np.random.rand(len(player_list)))],
            "% Shots on Goal": [round(x, 1) for x in (50 + (50 * np.random.rand(len(player_list))))],
            "Puck Battles Won, %": [round(x, 1) for x in (50 + (50 * np.random.rand(len(player_list))))],
            "Accurate Passes, %": [round(x, 1) for x in (60 + (40 * np.random.rand(len(player_list))))],
            "Faceoffs Won, %": [round(x, 1) for x in (40 + (60 * np.random.rand(len(player_list))))] if category != "Goalkeepers" else None,
            "Power Play, %": [round(x, 1) for x in (10 + (20 * np.random.rand(len(player_list))))],
            "Short-Handed, %": [round(x, 1) for x in (10 + (20 * np.random.rand(len(player_list))))],
        })
    return kpi_data

# Create KPI Table for a category
def category_kpi_table(kpi_data, category):
    # Generate headers based on the category
    headers = [
        "Player",
        "Goals" if category != "Goalkeepers" else "Saves",
        "Goals Against" if category != "Goalkeepers" else "Save %",
        "% Shots on Goal",
        "Puck Battles Won, %",
        "Accurate Passes, %",
        "Faceoffs Won, %" if category != "Goalkeepers" else None,
        "Power Play, %",
        "Short-Handed, %"
    ]
    headers = [h for h in headers if h is not None]  # Remove None values

    # Create header row
    header_row = dbc.Row(
        [dbc.Col(html.Div(header, style={"font-weight": "bold", "text-align": "center"}), width=1) for header in headers],
        style={"margin-bottom": "10px", "background-color": "#f8f9fa", "padding": "10px", "border-bottom": "1px solid #dee2e6"}
    )

    # Create rows for each player
    rows = []
    for _, row in kpi_data.iterrows():
        player_row = [
            dbc.Col(html.Div(row["Player"], style={"text-align": "left"}), width=1)
        ]
        for header in headers[1:]:  # Skip "Player" column
            value = row[header]
            color = (
                "success" if value >= 80 else "warning" if value >= 50 else "danger"
            )
            player_row.append(
                dbc.Col(
                    dbc.Progress(
                        value=min(value, 100),
                        color=color,
                        striped=True,
                        animated=True,
                        style={"height": "15px"}
                    ),
                    width=1
                )
            )
        rows.append(dbc.Row(player_row, style={"margin-bottom": "10px"}))

    return html.Div([header_row] + rows, style={"margin-top": "20px"})

# Main Layout
def layout(conn=None):
    kpi_data = get_player_kpi_data()

    sections = []
    for category, data in kpi_data.items():
        sections.append(html.H3(category, style={"margin-top": "20px"}))
        sections.append(category_kpi_table(data, category))

    return dbc.Container(
        [
            html.H2("Player Performance by Category", className="content-title"),
            html.Hr(),
            *sections,
        ],
        fluid=True,  # Ensures proper alignment with the sidebar
        style={"padding": "20px"}  # Adds padding for spacing
    )