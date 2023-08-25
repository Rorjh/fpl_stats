from dash import Dash, html, dcc, callback, Output, Input, _callback_context
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from layout import set_layout
from get_players_data import get_players_data
import requests

players = get_players_data()

app = Dash(__name__, title='FPL Dashboard', external_stylesheets=[dbc.themes.DARKLY, 'assets/ext_style.css'])

app.layout = set_layout(players)

@app.callback(
    Output("app_tabs", "active_tab"),
    Input("btn_tab_1", "n_clicks"),
    Input("btn_tab_2", "n_clicks"),
    Input("btn_tab_3", "n_clicks"),
    prevent_initial_call=True
)
def switch_tab(btn1, btn2, btn3):
    ctx = str(_callback_context.callback_context.triggered_id)
    active_tab_id = ctx.strip('btn_tab_')
    return active_tab_id

# @app.callback(
#     Output('team_pl1', 'options'),
#     Output('position_pl1', 'options'),
#     Output('pl1', 'options'),
#     # Output('team_pl2', 'value'),
#     # Output('position_pl2', 'value'),
#     # Output('pl2', 'value'),
#     Input('team_pl1', 'value'),
#     Input('position_pl1', 'value'),
#     Input('pl1', 'value'),
#     # Input('team_pl2', 'value'),
#     # Input('position_pl2', 'value'),
#     # Input('pl2', 'value'),
#     prevent_initial_call=True
# )
# def filter_players(team1, pos1, pl1, team2, pos2, pl2):
#     ctx = str(_callback_context.callback_context.triggered_id)
#     players = pd.DataFrame(r['elements'])
#     teams = pd.DataFrame(r['teams'])
#     positions = pd.DataFrame(r['element_types'])
#     players = players.merge(right=teams, left_on='team', right_on='id')
#     players = players.merge(right=positions, left_on='element_type', right_on='id')
#     if ctx == 'team_pl1':



if __name__ == '__main__':
    app.run(debug=True)