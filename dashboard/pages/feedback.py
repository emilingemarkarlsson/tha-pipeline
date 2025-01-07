from dash import html, dcc
import dash_bootstrap_components as dbc

def layout(conn=None):
    return html.Div([
        dbc.Container([
            html.H1("Feedback & Contact", className="text-center mb-4"),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Send us your thoughts", className="card-title"),
                            dbc.Input(
                                id="name-input",
                                placeholder="Your name",
                                type="text",
                                className="mb-3"
                            ),
                            dcc.Textarea(
                                id="feedback-textarea",
                                placeholder="Enter your feedback here...",
                                style={"width": "100%", "height": "150px"},
                                className="mb-3"
                            ),
                            html.H5("Preferred contact platform:", className="mt-3"),
                            dbc.RadioItems(
                                options=[
                                    {"label": "Email", "value": "email"},
                                    {"label": "Microsoft Teams", "value": "teams"},
                                    {"label": "Slack", "value": "slack"}
                                ],
                                value="email",
                                id="contact-platform",
                                inline=True,
                                className="mb-3"
                            ),
                            dbc.Button(
                                "Submit Feedback",
                                id="submit-feedback",
                                color="primary",
                                className="mt-3"
                            ),
                            html.Div(
                                id="feedback-response",
                                className="mt-3 text-success"
                            )
                        ])
                    ], className="shadow")
                ], width={"size": 8, "offset": 2})
            ])
        ], className="py-4")
    ])