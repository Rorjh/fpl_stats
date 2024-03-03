import requests
import pandas as pd
from bs4 import BeautifulSoup
from difflib import get_close_matches

def get_league_url(country:str, gender:str, season_end_year:int, tier:str):
    """Returns the url of a league for given country, tier, season and gender.

    Keyword arguments:
    country: string with country code.
    gender: string representig gender (one of ['M', 'F']).
    season_end_year: int value of a year in which season ended.
    tier: string repesenting the league tier ('1st', '2nd' etc.)
    """
    seasons = pd.read_csv("https://raw.githubusercontent.com/JaseZiv/worldfootballR_data/master/raw-data/all_leages_and_cups/all_competitions.csv")
    seasons = seasons[(seasons.country == country) & (seasons.tier == tier) & (seasons.gender == gender) & (seasons.season_end_year == season_end_year)]
    return seasons.seasons_urls.iloc[0]

def get_teams_urls(league_url:str):
    """Given url of a league it returns the dictionary with teams competing and corresponding urls.

    Keyword arguments:
    league_url: url of a league
    """
    r = requests.get(league_url, verify=False)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', id='stats_squads_standard_for')
    urls = table.find_all('a')
    urls = {link.text:link.get('href') for link in urls}
    return urls

def get_players_urls(team_url:str):
    """Given url of a team it returns the dictionary with players in squad and corresponding urls.

    Keyword arguments:
    team_url: url of a team
    """
    url_base = 'https://fbref.com/'
    r = requests.get(url_base+team_url, verify=False)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', id='stats_standard_9')
    ths = table.find_all('th')
    urls = [th.find('a') for th in ths]
    urls = [url for url in urls if url is not None]
    urls = {link.text:link.get('href') for link in urls}
    return urls

def get_scouting_report(player_url:str):
    """Given url of a player it returns the scouting report as DataFrame.

    Keyword arguments:
    player_url: url of a player
    """
    url_base = 'https://fbref.com/'
    r = requests.get(url_base+player_url, verify=False)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', id=lambda value: value and value.startswith('scout_summary_'))
    scouting_report = pd.read_html(str(table))[0]
    scouting_report = scouting_report.dropna()
    return scouting_report

def scouting_report_fpl(team, player, player_web_name):
    team_names_mapping = {
        "Luton": "Luton Town",
        "Man City": "Manchester City",
        "Man Utd": "Manchester Utd",
        "Newcastle": "Newcastle Utd",
        "Nott'm Forest": "Nott'ham Forest",
        "Spurs": "Tottenham"
    }
    if team in team_names_mapping.keys():
        team = team_names_mapping[team]
    
    # league_url = get_league_url(country = "ENG", gender = "M", season_end_year = 2024, tier = '1st')
    # teams_urls = get_teams_urls(league_url)
    # players_urls = get_players_urls(teams_urls[team])
    urls_df = pd.read_csv('data/fbref_epl_players_urls.csv')

    if player not in urls_df.player.to_list():
        if player_web_name in urls_df.player.to_list():
            player = player_web_name
        else:
            matches = get_close_matches(player, urls_df.player.to_list())
            if len(matches) == 0:
                matches = get_close_matches(player_web_name, urls_df.player.to_list())
            if len(matches) == 0:
                return None
            else:
                player = matches[0] 
    url = urls_df[urls_df.player == player]['url'].iloc[0]
    report = get_scouting_report(url)
    return report