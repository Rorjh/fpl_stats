from dash import Dash, html, dcc, callback, Output, Input, _callback_context, no_update, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from layout import set_layout
from get_players_data import get_players_data
import plotly.graph_objects as go
from fbref_scrapping import scouting_report_fpl

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
    prevent_initial_call = True
)
def compare_players(player1, player2, stats_type):
    data = []
    img_pl1 = html.Div(style={'width': '400px', 'justify': 'center'})
    img_pl2 = html.Div(style={'width': '400px', 'justify': 'center'})
    stats_table_1 = html.Div(style={'width': '400px', 'justify': 'center'})
    stats_table_2 = html.Div(style={'width': '400px', 'justify': 'center'})

    if player1 != None:
        player = players[players['full_name'] == player1]
        if stats_type == "Attacking":
            values = [
                player['goals_scored_per90'].astype(float).iloc[0]/players['goals_scored_per90'].astype(float).max(),
                player['assists_per90'].astype(float).iloc[0]/players['assists_per90'].astype(float).max(),
                player['total_points_per90'].astype(float).iloc[0]/players['total_points_per90'].astype(float).max(),
                player['expected_goals_per90'].astype(float).iloc[0]/players['expected_goals_per90'].astype(float).max(),
                player['expected_assists_per90'].astype(float).iloc[0]/players['expected_assists_per90'].astype(float).max(),
                player['influence'].astype(float).iloc[0]/players['influence'].astype(float).max(),
                player['creativity'].astype(float).iloc[0]/players['creativity'].astype(float).max(),
                player['threat'].astype(float).iloc[0]/players['threat'].astype(float).max()
            ]
            labels = ['Goals', 'Assists', 'Points', 'xG', 'xA', 'Influence', 'Creativity', 'Threat']
        elif stats_type == "Defending":
            values = [
                player['clean_sheets_per90'].astype(float).iloc[0]/players['clean_sheets_per90'].astype(float).max(),
                player['goals_conceded_per90'].astype(float).iloc[0]/players['goals_conceded_per90'].astype(float).max(),
                player['expected_goals_conceded_per90'].astype(float).iloc[0]/players['expected_goals_conceded_per90'].astype(float).max()
            ]
            labels = ['Clean Sheets', 'Goals Conceded', 'xGC']
        elif stats_type == "Goalkeepers":
            values = [
                player['clean_sheets_per90'].astype(float).iloc[0]/players['clean_sheets_per90'].astype(float).max(),
                player['goals_conceded_per90'].astype(float).iloc[0]/players['goals_conceded_per90'].astype(float).max(),
                player['expected_goals_conceded_per90'].astype(float).iloc[0]/players['expected_goals_conceded_per90'].astype(float).max(),
                player['penalties_saved_per90'].astype(float).iloc[0]/players['penalties_saved_per90'].astype(float).max(),
                player['saves_per90'].astype(float).iloc[0]/players['saves_per90'].astype(float).max()
            ]
            labels = ['Clean Sheets', 'Goals Conceded', 'xGC', 'Penalties Saved', 'Saves']

        try:
            scout_report  = scouting_report_fpl(player['name'].iloc[0], player['full_name'].iloc[0], player['web_name'].iloc[0])
            
            stats_table_1 = dash_table.DataTable(
                        data = scout_report.to_dict('records'),
                        columns = [{"name": i, "id": i} for i in scout_report.columns],
                        style_header={
                            'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'white'
                        },
                        style_data={
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': 'white'
                        },
                        style_table={'margin-top': '15px', 'width': '400px'},
                        page_action='none',
                    )

            if stats_type == "Attacking":
                scout_report = scout_report.iloc[[2,5,6,9,12]]
            elif stats_type == "Defending":
                scout_report = scout_report.iloc[[13,15,16,17]]
            elif stats_type == "Goalkeepers":
                scout_report = scout_report.iloc[[0,2,3,4]]

            values += [value/100 for value in scout_report['Percentile'].to_list()]
            labels += scout_report['Statistic'].to_list()
        except:
            stats_table_1 = html.Div('Scout report unavailable', style={'width': '400px', 'justify': 'center'})

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
                player['goals_scored_per90'].astype(float).iloc[0]/players['goals_scored_per90'].astype(float).max(),
                player['assists_per90'].astype(float).iloc[0]/players['assists_per90'].astype(float).max(),
                player['total_points_per90'].astype(float).iloc[0]/players['total_points_per90'].astype(float).max(),
                player['expected_goals_per90'].astype(float).iloc[0]/players['expected_goals_per90'].astype(float).max(),
                player['expected_assists_per90'].astype(float).iloc[0]/players['expected_assists_per90'].astype(float).max(),
                player['influence'].astype(float).iloc[0]/players['influence'].astype(float).max(),
                player['creativity'].astype(float).iloc[0]/players['creativity'].astype(float).max(),
                player['threat'].astype(float).iloc[0]/players['threat'].astype(float).max()
            ]
            labels = ['Goals', 'Assists', 'Points', 'xG', 'xA', 'Influence', 'Creativity', 'Threat']
        elif stats_type == "Defending":
            values = [
                player['clean_sheets_per90'].astype(float).iloc[0]/players['clean_sheets_per90'].astype(float).max(),
                player['goals_conceded_per90'].astype(float).iloc[0]/players['goals_conceded_per90'].astype(float).max(),
                player['expected_goals_conceded_per90'].astype(float).iloc[0]/players['expected_goals_conceded_per90'].astype(float).max()
            ]
            labels = ['Clean Sheets', 'Goals Conceded', 'xGC']
        elif stats_type == "Goalkeepers":
            values = [
                player['clean_sheets_per90'].astype(float).iloc[0]/players['clean_sheets_per90'].astype(float).max(),
                player['goals_conceded_per90'].astype(float).iloc[0]/players['goals_conceded_per90'].astype(float).max(),
                player['expected_goals_conceded_per90'].astype(float).iloc[0]/players['expected_goals_conceded_per90'].astype(float).max(),
                player['penalties_saved_per90'].astype(float).iloc[0]/players['penalties_saved_per90'].astype(float).max(),
                player['saves_per90'].astype(float).iloc[0]/players['saves_per90'].astype(float).max()
            ]
            labels = ['Clean Sheets', 'Goals Conceded', 'xGC', 'Penalties Saved', 'Saves']

        try:
            scout_report  = scouting_report_fpl(player['name'].iloc[0], player['full_name'].iloc[0], player['web_name'].iloc[0])
            stats_table_2 = dash_table.DataTable(
                        data = scout_report.to_dict('records'),
                        columns = [{"name": i, "id": i} for i in scout_report.columns],
                        style_header={
                            'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'white'
                        },
                        style_data={
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': 'white'
                        },
                        style_table={'margin-top': '15px', 'width': '400px'},
                        page_action='none',
                    )
 
            if stats_type == "Attacking":
                scout_report = scout_report.iloc[[2,5,6,9,12]]
            elif stats_type == "Defending":
                scout_report = scout_report.iloc[[13,15,16,17]]
            elif stats_type == "Goalkeepers":
                scout_report = scout_report.iloc[[0,2,3,4]]

            values += [value/100 for value in scout_report['Percentile'].to_list()]
            labels += scout_report['Statistic'].to_list()
        except:
            stats_table_2 = html.Div('Scout report unavailable', style={'width': '400px', 'justify': 'center'})
        
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
        )
    )
    
    figure = go.Figure(data=data, layout=layout)
    results = dbc.Row([
        dbc.Col([img_pl1, stats_table_1]),
        dbc.Col([dcc.Graph(figure=figure, style={'width': '600px', 'justify': 'center'})]),
        dbc.Col([img_pl2, stats_table_2]),
    ])

    return results


if __name__ == '__main__':
    app.run(debug=True)