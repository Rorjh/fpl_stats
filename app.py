from dash import Dash, html, dcc, callback, Output, Input, _callback_context, no_update
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from layout import set_layout
from get_players_data import get_players_data
import plotly.graph_objects as go

players = get_players_data()

app = Dash(__name__, title='FPL Dashboard', external_stylesheets=[dbc.themes.DARKLY, 'assets/ext_style.css'])
server = app.server

app.layout = set_layout(players)

@app.callback(
    Output("app_tabs", "active_tab"),
    Input("btn_tab_1", "n_clicks"),
    Input("btn_tab_2", "n_clicks"),
    prevent_initial_call=True
)
def switch_tab(btn1, btn2):
    ctx = str(_callback_context.callback_context.triggered_id)
    active_tab_id = ctx.strip('btn_tab_')
    return active_tab_id

# TODO: filters players by team and positions:
@app.callback(
    Output('player1', 'options'),
    Output('player2', 'options'),
    Input('team_pl1', 'value'),
    Input('position_pl1', 'value'),
    Input('team_pl2', 'value'),
    Input('position_pl2', 'value'),
    prevent_initial_call=True
)
def filter_players(team1, pos1, team2, pos2):
    if team1 != None and pos1 != None:
        team1_options = players[(players['name']==team1) & (players['singular_name']==pos1)]['full_name'].to_list()
    elif team1 == None and pos1 != None:
        team1_options = players[players['singular_name']==pos1]['full_name'].to_list()
    elif team1 != None and pos1 == None:
        team1_options = players[players['name']==team1]['full_name'].to_list()
    else:
        team1_options = no_update
    
    if team2 != None and pos2 != None:
        team2_options = players[(players['name']==team2) & (players['singular_name']==pos2)]['full_name'].to_list()
    elif team2 == None and pos2 != None:
        team2_options = players[players['singular_name']==pos2]['full_name'].to_list()
    elif team2 != None and pos2 == None:
        team2_options = players[players['name']==team2]['full_name'].to_list()
    else:
        team2_options = no_update

    return team1_options, team2_options

@app.callback(
    Output('compare_plot','children'),
    Input('player1', 'value'),
    Input('player2', 'value'),
    Input('stats_type', 'value'),
    Input('time_period', 'value'),
    prevent_initial_call = True
)
def compare_players(player1, player2, stats_type, period):
    data = []
    img_pl1 = html.Div(style={'width': '400px', 'justify': 'center'})
    img_pl2 = html.Div(style={'width': '400px', 'justify': 'center'})

    if player1 != None:
        player = players[players['full_name'] == player1]
        if stats_type == "Attacking":
            values = [
                player['goals_scored'].astype(float).iloc[0]/players['goals_scored'].astype(float).max(),
                player['assists'].astype(float).iloc[0]/players['assists'].astype(float).max(),
                player['total_points'].astype(float).iloc[0]/players['total_points'].astype(float).max(),
                player['expected_goals'].astype(float).iloc[0]/players['expected_goals'].astype(float).max(),
                player['expected_assists'].astype(float).iloc[0]/players['expected_assists'].astype(float).max(),
                player['influence'].astype(float).iloc[0]/players['influence'].astype(float).max(),
                player['creativity'].astype(float).iloc[0]/players['creativity'].astype(float).max(),
                player['threat'].astype(float).iloc[0]/players['threat'].astype(float).max()
            ]
            labels = ['Goals', 'Assists', 'Points', 'xG', 'xA', 'Influence', 'Creativity', 'Threat']
        elif stats_type == "Defending":
            values = [
                player['clean_sheets'].astype(float).iloc[0]/players['clean_sheets'].astype(float).max(),
                player['goals_conceded'].astype(float).iloc[0]/players['goals_conceded'].astype(float).max(),
                player['expected_goals_conceded'].astype(float).iloc[0]/players['expected_goals_conceded'].astype(float).max()
            ]
            labels = ['Clean Sheets', 'Goals Conceded', 'xGC']
        elif stats_type == "Goalkeepers":
            values = [
                player['clean_sheets'].astype(float).iloc[0]/players['clean_sheets'].astype(float).max(),
                player['goals_conceded'].astype(float).iloc[0]/players['goals_conceded'].astype(float).max(),
                player['expected_goals_conceded'].astype(float).iloc[0]/players['expected_goals_conceded'].astype(float).max(),
                player['penalties_saved'].astype(float).iloc[0]/players['penalties_saved'].astype(float).max(),
                player['saves'].astype(float).iloc[0]/players['saves'].astype(float).max()
            ]
            labels = ['Clean Sheets', 'Goals Conceded', 'xGC', 'Penalties Saved', 'Saves']
        
        if period == 'Per 90 min':
            values = [value/player['minutes'].astype(float).iloc[0]*90 for value in values]
        elif period == 'Per Start':
            values = [value/player['starts'].astype(float).iloc[0] for value in values]

        plt1 = go.Scatterpolar(
            r=values,
            theta=labels,
            fill='toself',
            name=player1,
            hoverinfo='skip'
        )
        data.append(plt1)
        player_id = player['code_x'].iloc[0]
        img_pl1 = html.Img(src="https://resources.premierleague.com/premierleague/photos/players/110x140/p{}.png".format(player_id), style={'width': '400px', 'justify': 'center'})
    
    if player2 != None:
        player = players[players['full_name'] == player2]
        if stats_type == "Attacking":
            values = [
                player['goals_scored'].astype(float).iloc[0]/players['goals_scored'].astype(float).max(),
                player['assists'].astype(float).iloc[0]/players['assists'].astype(float).max(),
                player['total_points'].astype(float).iloc[0]/players['total_points'].astype(float).max(),
                player['expected_goals'].astype(float).iloc[0]/players['expected_goals'].astype(float).max(),
                player['expected_assists'].astype(float).iloc[0]/players['expected_assists'].astype(float).max(),
                player['influence'].astype(float).iloc[0]/players['influence'].astype(float).max(),
                player['creativity'].astype(float).iloc[0]/players['creativity'].astype(float).max(),
                player['threat'].astype(float).iloc[0]/players['threat'].astype(float).max()
            ]
            labels = ['Goals', 'Assists', 'Points', 'xG', 'xA', 'Influence', 'Creativity', 'Threat']
        elif stats_type == "Defending":
            values = [
                player['clean_sheets'].astype(float).iloc[0]/players['clean_sheets'].astype(float).max(),
                player['goals_conceded'].astype(float).iloc[0]/players['goals_conceded'].astype(float).max(),
                player['expected_goals_conceded'].astype(float).iloc[0]/players['expected_goals_conceded'].astype(float).max()
            ]
            labels = ['Clean Sheets', 'Goals Conceded', 'xGC']
        elif stats_type == "Goalkeepers":
            values = [
                player['clean_sheets'].astype(float).iloc[0]/players['clean_sheets'].astype(float).max(),
                player['goals_conceded'].astype(float).iloc[0]/players['goals_conceded'].astype(float).max(),
                player['expected_goals_conceded'].astype(float).iloc[0]/players['expected_goals_conceded'].astype(float).max(),
                player['penalties_saved'].astype(float).iloc[0]/players['penalties_saved'].astype(float).max(),
                player['saves'].astype(float).iloc[0]/players['saves'].astype(float).max()
            ]
            labels = ['Clean Sheets', 'Goals Conceded', 'xGC', 'Penalties Saved', 'Saves']
        
        if period == 'Per 90 min':
            values = [value/player['minutes'].astype(float).iloc[0]*90 for value in values]
        elif period == 'Per Start':
            values = [value/player['starts'].astype(float).iloc[0] for value in values]
        
        plt2 = go.Scatterpolar(
            r=values,
            theta=labels,
            fill='toself',
            name=player2,
            hoverinfo='skip'
        )
        data.append(plt2)
        player_id = player['code_x'].iloc[0]
        img_pl2 = html.Img(src="https://resources.premierleague.com/premierleague/photos/players/110x140/p{}.png".format(player_id), style={'width': '400px', 'justify': 'center'})
    
    layout = go.Layout(
        polar = dict(
            radialaxis = dict(showticklabels = False)
        ),
        title=period
    )
    
    figure = go.Figure(data=data, layout=layout)
    results = [
        img_pl1,
        dcc.Graph(figure=figure, style={'width': '600px', 'justify': 'center'}),
        img_pl2    
    ]

    return results


if __name__ == '__main__':
    app.run(debug=True)