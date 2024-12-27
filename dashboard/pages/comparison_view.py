from dash import html, dcc
import plotly.express as px
import pandas as pd

# Hämta data från DuckDB eller använd dummy-data
data = pd.DataFrame({
    "KPI": ["Mål", "Assist", "Vunna tekningar", "Utvisningar", "Skott på mål"],
    "Laget": [10, 20, 30, 5, 25],
    "Spelare": [8, 15, 25, 3, 20],
})

# Skapa en graf för KPI
fig = px.bar(data, x="KPI", y=["Laget", "Spelare"], barmode="group", title="KPI-översikt")

# Layout för KPI-vyn
layout = html.Div([
    html.H2("KPI-översikt", className="text-center"),
    html.P("Se hur laget och spelarna presterar i nyckelområden."),
    dcc.Graph(figure=fig),
])