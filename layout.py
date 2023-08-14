from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

def set_layout(r):
    players = pd.DataFrame(r['elements'])
    teams = pd.DataFrame(r['teams'])
    players = players.merge(right=teams, left_on='team', right_on='id')
    top_scorers = players[players.goals_scored != 0].sort_values('goals_scored', ascending=False)[['first_name','second_name','name','goals_scored','expected_goals']]
    top_assisters = players[players.assists != 0].sort_values('assists', ascending=False)[['first_name','second_name','name','assists','expected_assists']]
    players['now_cost'] = players['now_cost'] / 10
    positions = pd.DataFrame(r['element_types'])
    players = players.merge(right=positions, left_on='element_type', right_on='id')
    players['expected_goal_involvements'] = players['expected_goal_involvements'].astype(float)
    players['expected_goals_conceded'] = players['expected_goals_conceded'].astype(float)

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
                dbc.Button("Players Data", 'btn_tab_2'),
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
                html.P("This is tab 2!", className="card-text")
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