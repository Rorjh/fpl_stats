from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from layout import set_layout
import requests

base_url = 'https://fantasy.premierleague.com/api/' 
r = requests.get(base_url+'bootstrap-static/').json()

app = Dash(__name__, title='FPL Dashboard', external_stylesheets=[dbc.themes.DARKLY])

app.layout = set_layout(r)

if __name__ == '__main__':
    app.run(debug=True)