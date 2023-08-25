from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

def set_layout(players):
    
    top_scorers = players[players.goals_scored != 0].sort_values('goals_scored', ascending=False)[['first_name','second_name','name','goals_scored','expected_goals']]
    top_assisters = players[players.assists != 0].sort_values('assists', ascending=False)[['first_name','second_name','name','assists','expected_assists']]

    navbar = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src='assets/prem-logo-white.png', height="30px")),
                            dbc.Col(dbc.NavbarBrand("FPL Dashboard", className="ms-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="http://127.0.0.1:8050/",
                    style={"textDecoration": "none"},
                ),
                dbc.Button("General Data", 'btn_tab_1'),
                dbc.Button("Players Comparison", 'btn_tab_2'),
                dbc.Button("My Team", 'btn_tab_3'),
            ],
            style={'justify':'left'}
        ),
        color="dark",
        dark=True,
    )

    # Define the layout for each tab
    tab1_content = html.Div([
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4('Top Scorers'),
                dash_table.DataTable(
                    data = top_scorers.to_dict('records'),
                    columns = [{"name": i, "id": i} for i in top_scorers.columns],
                    style_header={
                        'backgroundColor': 'rgb(30, 30, 30)',
                        'color': 'white'
                    },
                    style_data={
                        'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white'
                    },
                    style_table={'height': '400px', 'overflowY': 'auto'},
                    page_action='none',
                )
            ])), width=6),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4('Top Assisters'),
                dash_table.DataTable(
                    data = top_assisters.to_dict('records'),
                    columns = [{"name": i, "id": i} for i in top_assisters.columns],
                    style_header={
                        'backgroundColor': 'rgb(30, 30, 30)',
                        'color': 'white'
                    },
                    style_data={
                        'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white'
                    },
                    style_table={'height': '400px', 'overflowY': 'auto'},
                    page_action='none',
                )
            ])), width=6),
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4('xGI vs Price'),
                dcc.Graph(
                    figure=px.scatter(players, x="now_cost", y="expected_goal_involvements", color="singular_name", hover_data=['first_name','second_name'])
                )
            ])), width=6),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4('xGC vs Price'),
                dcc.Graph(
                    figure=px.scatter(players, x="now_cost", y="expected_goals_conceded", color="singular_name", hover_data=['first_name','second_name'])
                )
            ])), width=6),
        ], style={'margin-top': '20px'}),
    ],style={'margin':'10px 10px 10xp 10px'})
      
    tab2_content = dbc.Card(
        dbc.CardBody(
            [
                dbc.Row([
                    dbc.Col([
                        html.H4('Player 1'),
                        dcc.Dropdown(list(set(players['name'].to_list())), id='team_pl1', placeholder='Select Team', clearable=True, style={"color":"black"}),
                        dcc.Dropdown(list(set(players['singular_name'].to_list())), id='position_pl1', placeholder='Select Position', clearable=True, style={"color":"black", "margin-top":"10px"}),
                        dcc.Dropdown(players['full_name'].to_list(), id='player1', placeholder='Select Player', clearable=True, style={"color":"black", "margin-top":"10px"})
                    ]),
                    dbc.Col([
                        html.H4('Player 2'),
                        dcc.Dropdown(list(set(players['name'].to_list())), id='team_pl2', placeholder='Select Team', clearable=True, style={"color":"black"}),
                        dcc.Dropdown(list(set(players['singular_name'].to_list())), id='position_pl2', placeholder='Select Position', clearable=True, style={"color":"black", "margin-top":"10px"}),
                        dcc.Dropdown(players['full_name'].to_list(), id='player2', placeholder='Select Player', clearable=True, style={"color":"black", "margin-top":"10px"})
                    ])
                ])
            ]
        ),
        className="mt-3",
    )

    tab3_content = dbc.Card(
        dbc.CardBody(
            [
                html.P("This is tab 3!", className="card-text")
            ]
        ),
        className="mt-3",
    )

    tabs = dbc.Tabs([
        dbc.Tab(tab1_content, label='Players Data', tab_id='1'),
        dbc.Tab(tab2_content, label='Team Planner', tab_id='2'),
        dbc.Tab(tab3_content, label='Tab3', tab_id='3'),
    ], style={'margin-top':'20px'}, id='app_tabs', active_tab='1')


    layout = dbc.Container(
        children=[navbar, tabs],
        fluid=True,
        style={
            'display': 'flex',
            'min-height': '100vh',
            'flex-direction': 'column',
            'min-width': 'fit-content'
        }
    )

    return layout