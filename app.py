from dash import Dash, html, dcc, callback, Output, Input, _callback_context
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from layout import set_layout
import requests

base_url = 'https://fantasy.premierleague.com/api/' 
r = requests.get(base_url+'bootstrap-static/').json()

app = Dash(__name__, title='FPL Dashboard', external_stylesheets=[dbc.themes.DARKLY, 'assets/ext_style.css'])

app.layout = set_layout(r)

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
if __name__ == '__main__':
    app.run(debug=True)