from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Generate fake data for Organization Key Stats
def get_organization_kpi_data():
    return pd.DataFrame({
        "KPI": [
            "Revenue ($)", "Goals Scored", "Goals Against", "Average Attendance",
            "Power Play Efficiency (%)", "Faceoff Win Rate (%)", "Membership Growth",
            "Diversity (%)", "Costs ($)"
        ],
        "Current Value": [900000, 125, 85, 7500, 25, 55, 400, 30, 600000],  # Replace with realistic values
        "Target Value": [1000000, 150, 80, 10000, 30, 60, 500, 40, 500000],  # Replace with realistic targets
        "Progress (%)": [90.0, 83.3, 106.3, 75.0, 83.3, 91.7, 80.0, 75.0, 120.0],  # Progress based on current/target
    })

# Generate fake data for trends over seasons
def get_organization_trend_data():
    seasons = [f"{year}-{year + 1}" for year in range(2015, 2023)]
    return pd.DataFrame({
        "Season": seasons,
        "Revenue": [500000, 600000, 700000, 800000, 850000, 900000, 950000, 1000000],
        "Goals Scored": [100, 110, 120, 125, 130, 140, 145, 150],
        "Goals Against": [90, 85, 80, 78, 75, 73, 72, 70],
        "Attendance": [5000, 6000, 7000, 7500, 8000, 8500, 9000, 9500],
        "Power Play Efficiency": [10, 15, 20, 22, 25, 27, 28, 30],
        "Faceoff Win Rate": [45, 48, 50, 52, 54, 55, 57, 60],
        "Diversity": [20, 22, 25, 27, 30, 33, 35, 40],
    })

# Create KPI Table with Progress Bars
def organization_kpi_table(kpi_data):
    rows = []
    for _, row in kpi_data.iterrows():
        color = "success" if row["Progress (%)"] >= 80 else "warning" if row["Progress (%)"] >= 50 else "danger"
        rows.append(
            dbc.Row(
                [
                    dbc.Col(html.Div(row["KPI"], style={"font-weight": "bold", "text-align": "center"}), width=2),
                    dbc.Col(html.Div(f"{row['Current Value']:,} / {row['Target Value']:,}", style={"text-align": "center"}), width=2),
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
def organization_trend_graphs(trend_data):
    graphs = []
    for column in trend_data.columns[1:]:
        fig = px.line(
            trend_data,
            x="Season",
            y=column,
            title=f"{column} Over Seasons",
            markers=True,
            line_shape="spline",
            labels={column: column, "Season": "Season"}
        )
        fig.update_traces(line_color="#233762")
        fig.update_layout(margin={"l": 10, "r": 10, "t": 40, "b": 40})
        graphs.append(dcc.Graph(figure=fig, style={"height": "300px"}))
    return graphs

# Main Layout
def layout(conn=None):
    kpi_data = get_organization_kpi_data()
    trend_data = get_organization_trend_data()

    kpi_section = organization_kpi_table(kpi_data)
    trend_section = organization_trend_graphs(trend_data)

    return dbc.Container(
        [
            html.H2("Organization Key Stats", className="content-title"),
            html.Hr(),
            html.Div(kpi_section),
            html.Br(),
            html.H4("KPI Trends Over Seasons"),
            dbc.Row([dbc.Col(graph, width=6) for graph in trend_section]),
        ],
        fluid=True,  # Ensures proper alignment with the sidebar
        style={"padding": "20px"}  # Adds padding for spacing
    )