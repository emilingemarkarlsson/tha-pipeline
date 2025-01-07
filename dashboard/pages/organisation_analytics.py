from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

# Dummy Data for Visualization
import pandas as pd
import numpy as np

# Dummy data for example purposes
def get_dummy_data():
    seasons = [f"{year}-{year+1}" for year in range(2015, 2023)]
    return pd.DataFrame({
        "season": seasons,
        "goals_scored": np.random.randint(100, 150, len(seasons)),
        "goals_against": np.random.randint(80, 120, len(seasons)),
        "games_won": np.random.randint(20, 40, len(seasons)),
        "games_lost": np.random.randint(10, 20, len(seasons)),
        "attendance": np.random.randint(5000, 10000, len(seasons)),
        "members": np.random.randint(200, 400, len(seasons)),
        "power_play_efficiency": np.random.uniform(10, 30, len(seasons)),
        "faceoff_win_rate": np.random.uniform(40, 60, len(seasons)),
        "revenue": np.random.randint(500000, 1000000, len(seasons)),
        "costs": np.random.randint(300000, 700000, len(seasons)),
        "diversity_percentage": np.random.uniform(10, 40, len(seasons)),
    })

# Layout for the Overview Tab
def overview_tab(data):
    # KPIs
    goals_total = data["goals_scored"].sum()
    games_won = data["games_won"].sum()
    avg_attendance = data["attendance"].mean()
    total_members = data["members"].sum()

    # KPI Cards
    kpi_cards = dbc.Row(
        [
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Total Goals Scored", className="card-title"),
                    html.H2(f"{goals_total}", className="card-text"),
                ])
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Games Won", className="card-title"),
                    html.H2(f"{games_won}", className="card-text"),
                ])
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Average Attendance", className="card-title"),
                    html.H2(f"{avg_attendance:.0f}", className="card-text"),
                ])
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Total Members", className="card-title"),
                    html.H2(f"{total_members}", className="card-text"),
                ])
            ]), width=3),
        ]
    )

    # Charts
    goals_fig = go.Figure()
    goals_fig.add_trace(go.Bar(
        x=data["season"],
        y=data["goals_scored"],
        name="Goals Scored",
        marker_color="#5EC577",
    ))
    goals_fig.add_trace(go.Bar(
        x=data["season"],
        y=data["goals_against"],
        name="Goals Against",
        marker_color="#D64550",
    ))
    goals_fig.update_layout(
        title="Goals Scored vs Goals Against by Season",
        barmode="group",
        xaxis_title="Season",
        yaxis_title="Goals",
        height=400,
    )

    attendance_fig = px.line(
        data, 
        x="season", 
        y="attendance", 
        title="Average Attendance Per Season",
        markers=True,
        line_shape="spline"
    )
    attendance_fig.update_traces(line_color="#233762")

    # Layout
    return html.Div([
        html.H2("Overview", className="content-title"),
        kpi_cards,
        html.Br(),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=goals_fig), width=6),
            dbc.Col(dcc.Graph(figure=attendance_fig), width=6),
        ]),
    ])

# Layout for the Performance Tab
def performance_tab(data):
    power_play_fig = px.bar(
        data,
        x="season",
        y="power_play_efficiency",
        title="Power Play Efficiency by Season",
        labels={"power_play_efficiency": "Power Play Efficiency (%)", "season": "Season"},
        color="power_play_efficiency",
        color_continuous_scale=["#5EC577", "#D64550"],  # Green to Red gradient
    )

    faceoff_fig = px.line(
        data,
        x="season",
        y="faceoff_win_rate",
        title="Faceoff Win Rate by Season",
        labels={"faceoff_win_rate": "Faceoff Win Rate (%)", "season": "Season"},
        markers=True,
        line_shape="spline",
    )
    faceoff_fig.update_traces(line_color="#233762")

    return html.Div([
        html.H2("Performance Metrics", className="content-title"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=power_play_fig), width=6),
            dbc.Col(dcc.Graph(figure=faceoff_fig), width=6),
        ]),
    ])

# Layout for the Membership Tab
def membership_tab(data):
    member_fig = px.bar(
        data,
        x="season",
        y="members",
        title="Total Members by Season",
        labels={"members": "Total Members", "season": "Season"},
        color="members",
        color_continuous_scale="Blues",
    )

    return html.Div([
        html.H2("Membership Metrics", className="content-title"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=member_fig), width=12),
        ]),
    ])

# Layout for the Fan Engagement Tab
def fan_engagement_tab(data):
    engagement_fig = px.bar(
        data,
        x="season",
        y="attendance",
        title="Fan Engagement (Attendance) by Season",
        labels={"attendance": "Attendance", "season": "Season"},
        color="attendance",
        color_continuous_scale="Viridis",
    )

    return html.Div([
        html.H2("Fan Engagement Metrics", className="content-title"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=engagement_fig), width=12),
        ]),
    ])

# Layout for the Financials Tab
def financials_tab(data):
    revenue_cost_fig = go.Figure()
    revenue_cost_fig.add_trace(go.Bar(
        x=data["season"],
        y=data["revenue"],
        name="Revenue",
        marker_color="#5EC577",
    ))
    revenue_cost_fig.add_trace(go.Bar(
        x=data["season"],
        y=data["costs"],
        name="Costs",
        marker_color="#D64550",
    ))
    revenue_cost_fig.update_layout(
        title="Revenue vs Costs by Season",
        barmode="group",
        xaxis_title="Season",
        yaxis_title="Amount ($)",
        height=400,
    )

    return html.Div([
        html.H2("Financial Metrics", className="content-title"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=revenue_cost_fig), width=12),
        ]),
    ])

# Layout for the Diversity & Inclusion Tab
def diversity_inclusion_tab(data):
    diversity_fig = px.bar(
        data,
        x="season",
        y="diversity_percentage",
        title="Diversity Percentage by Season",
        labels={"diversity_percentage": "Diversity (%)", "season": "Season"},
        color="diversity_percentage",
        color_continuous_scale=["#D64550", "#5EC577"],  # Red to Green gradient
    )

    return html.Div([
        html.H2("Diversity & Inclusion Metrics", className="content-title"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=diversity_fig), width=12),
        ]),
    ])

# Layout for the Innovation Tab
def innovation_tab(data):
    # Dummy data for innovation
    initiatives = pd.DataFrame({
        "season": data["season"],
        "new_agreements": np.random.randint(0, 10, len(data["season"])),
        "revenue_ideas": np.random.randint(0, 5, len(data["season"])),
        "training_innovations": np.random.randint(0, 7, len(data["season"])),
        "community_programs": np.random.randint(0, 8, len(data["season"])),
    })

    # KPI Cards
    kpi_cards = dbc.Row(
        [
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("New Agreements", className="card-title"),
                    html.H2(f"{initiatives['new_agreements'].sum()}", className="card-text"),
                ])
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Revenue Ideas", className="card-title"),
                    html.H2(f"{initiatives['revenue_ideas'].sum()}", className="card-text"),
                ])
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Training Innovations", className="card-title"),
                    html.H2(f"{initiatives['training_innovations'].sum()}", className="card-text"),
                ])
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Community Programs", className="card-title"),
                    html.H2(f"{initiatives['community_programs'].sum()}", className="card-text"),
                ])
            ]), width=3),
        ]
    )

    # Chart for Total Initiatives by Season
    initiatives_fig = go.Figure()
    initiatives_fig.add_trace(go.Bar(
        x=initiatives["season"],
        y=initiatives["new_agreements"],
        name="New Agreements",
        marker_color="#5EC577",
    ))
    initiatives_fig.add_trace(go.Bar(
        x=initiatives["season"],
        y=initiatives["revenue_ideas"],
        name="Revenue Ideas",
        marker_color="#D64550",
    ))
    initiatives_fig.add_trace(go.Bar(
        x=initiatives["season"],
        y=initiatives["training_innovations"],
        name="Training Innovations",
        marker_color="#233762",
    ))
    initiatives_fig.add_trace(go.Bar(
        x=initiatives["season"],
        y=initiatives["community_programs"],
        name="Community Programs",
        marker_color="#FFD700",
    ))
    initiatives_fig.update_layout(
        title="Innovation Initiatives by Season",
        barmode="stack",
        xaxis_title="Season",
        yaxis_title="Number of Initiatives",
        height=500,
    )

    # Layout
    return html.Div([
        html.H2("Innovation Metrics", className="content-title"),
        kpi_cards,
        html.Br(),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=initiatives_fig), width=12),
        ]),
    ])

def activities_tab(data):
    # Create dummy data for ice training hours
    training_data = pd.DataFrame({
        'Team': ['Senior', 'U20', 'U18', 'U16', 'U14'],
        'Hours_2023': [520, 480, 450, 400, 350],
        'Hours_2022': [500, 460, 430, 380, 330]
    })
    
    # Reshape data for plotting
    training_data_melted = pd.melt(
        training_data, 
        id_vars=['Team'], 
        value_vars=['Hours_2023', 'Hours_2022'],
        var_name='Season',
        value_name='Hours'
    )
    
    # Create bar chart
    training_fig = px.bar(
        training_data_melted,
        x='Team',
        y='Hours',
        color='Season',
        barmode='group',
        title='Ice Training Hours by Team and Season',
        labels={'Hours': 'Training Hours'}
    )

    return html.Div([
        dbc.Row([
            dbc.Col(
                html.H4("Activities Overview"),
                width=12
            )
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=training_fig),
                width=12
            )
        ])
    ])

# Main Layout Function
def layout(conn=None):
    # Load data (replace with actual database query)
    data = get_dummy_data()

    # Tabs with active_tab and ids
    tabs = dbc.Tabs(
        [
            dbc.Tab(overview_tab(data), label="Overview", tab_id="tab-0"),
            dbc.Tab(performance_tab(data), label="Performance", tab_id="tab-1"),
            dbc.Tab(membership_tab(data), label="Membership", tab_id="tab-2"),
            dbc.Tab(fan_engagement_tab(data), label="Fan Engagement", tab_id="tab-3"),
            dbc.Tab(financials_tab(data), label="Financials", tab_id="tab-4"),
            dbc.Tab(diversity_inclusion_tab(data), label="Diversity & Inclusion", tab_id="tab-5"),
            dbc.Tab(innovation_tab(data), label="Innovation", tab_id="tab-6"),
            dbc.Tab(activities_tab(data), label="Activity", tab_id="tab-7"), 
        ],
        active_tab="tab-0",
        id="tabs"
    )

    return html.Div([
        tabs
    ])