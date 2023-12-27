import requests
import pandas as pd

def get_players_data():
    base_url = 'https://fantasy.premierleague.com/api/' 
    r = requests.get(base_url+'bootstrap-static/').json()
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
    players['full_name'] = players['first_name']+' '+players['second_name']

    return players