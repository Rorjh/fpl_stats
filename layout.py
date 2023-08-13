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
        ]),
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

    # Define the main layout with tabs
    layout = html.Div([
        dbc.Row([dbc.Col(html.Img(src='assets/prem-logo-white.png', height='50px'),width=1),dbc.Col(html.H2('FPL Dashboard'),width=11)]),
        dbc.Tabs([
            dbc.Tab(tab1_content, label='Players Data'),
            dbc.Tab(tab2_content, label='Team Planner'),
            dbc.Tab(tab3_content, label='Tab3'),
        ], style={'margin-top':'20px'})
    ])

    return layout