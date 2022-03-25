import bs4
from bs4 import BeautifulSoup
import pandas as pd

import time
import re
from typing import Tuple


def get_match_count(soup: bs4.BeautifulSoup) -> Tuple[int, bs4.element.Tag]:

    data = soup.find_all('div')[16]
    game_count = soup.find_all('div', attrs = {'class': 'collapse navbar-collapse'})[1]
    
    if len(game_count.find_all('li')) == 3:
        match_count = 1
    elif len(game_count.find_all('li')) == 4:
        match_count = 2
    elif len(game_count.find_all('li')) == 5:
        match_count = 3
    elif len(game_count.find_all('li')) == 6:
        match_count = 4
    elif len(game_count.find_all('li')) == 7:
        match_count = 5
    else:
        match_count = None
        
    return int(match_count), data


def get_general_data(data: bs4.element.Tag, active_url: str) -> pd.Series:
    
    pattern = '\d{1,}'
    result = re.search(pattern, active_url)
    match_id = result.group(0)
    
    match_date = data.find('div', attrs={'class': 'col-12 col-sm-5 text-right'}).text
    team_names = data.find('h1').text.split('vs')
    tournament_name = data.find('a').text
    game_time = data.find('div', attrs={'class': 'col-6 text-center'}).find('h1').text

    index = ['Match_id', 'Date', 'Left_Team', 'Right_Team', 'Tournament', 'Time']
    general_data_series = pd.Series([match_id, match_date, team_names[0], team_names[1], tournament_name, game_time], index=index)
    
    return general_data_series


def get_left_team_stats(data: bs4.element.Tag, match_id: int, match_count_i: int) -> pd.Series:
    '''match_count_i is iteration in for loop when scrapper working.'''
    
    l_team_name = l_team_result = data.find('div', attrs={'class': 'row rowbreak pb-3'}).text.strip().replace('\n', '').split('-')[0]
    l_team_result = data.find('div', attrs={'class': 'row rowbreak pb-3'}).text.replace(' ', '').replace('\n', '').split('-')[1]
    kills_l_counts = data.find('div', attrs={'class': 'col-2'}).text.replace(' ', '').replace('\n', '')
    
    if len(data.find('div', attrs={'class': 'col-2'})) == 4:
        first_blood_l = 1
    else:
        first_blood_l = 0
        
    towers_l_count = data.find_all('div', attrs={'class': 'col-2'})[1].text.replace(' ', '').replace('\n', '')
    
    if len(data.find_all('div', attrs={'class': 'col-2'})[1]) == 4:
        first_tower_l = 1
    else:
        first_tower_l = 0
        
    dragons_l_count = data.find_all('div', attrs={'class': 'col-2'})[2].text.replace(' ', '').replace('\n', '')
    baron_l_count = data.find_all('div', attrs={'class': 'col-2'})[3].text.replace(' ', '').replace('\n', '')
    gold_l_count = data.find_all('div', attrs={'class': 'col-2'})[4].text.replace(' ', '').replace('\n', '')
    
    bans_l_team = []
    for i in range(5):
        bans_l_team.append(data.find_all('div', attrs={'class': 'col-10'})[0].find_all('a')[i].get('title').split()[0])
        
    picks_l_team = []
    for i in range(5):
        picks_l_team.append(data.find_all('div', attrs={'class': 'col-10'})[1].find_all('a')[i].get('title').split()[0])
    
    index = ['Name', 'Result', 'Kills', 'First_Blood', 'Towers', 'First_Tower', 'Dragons', 'Barons', 'Gold', 'Bans', 'Picks', 'Match_id', 'Match_count']
    left_team_stats = pd.Series([l_team_name, l_team_result, kills_l_counts, first_blood_l, towers_l_count, first_tower_l, dragons_l_count, baron_l_count, gold_l_count, bans_l_team, picks_l_team, match_id, match_count_i], index=index)

    return left_team_stats


def get_right_team_stats(data: bs4.element.Tag, match_id: int, match_count_i: int) -> pd.Series:
    
    r_team_name = data.find('div', attrs={'class': 'col-12 red-line-header'}).text.strip().replace('\n', '').split('-')[0]
    r_team_result = data.find('div', attrs={'class': 'col-12 red-line-header'}).text.replace(' ', '').replace('\n', '').split('-')[1]
    kills_r_count = data.find_all('div', attrs={'class': 'col-2'})[8].text.replace(' ', '').replace('\n', '')
    towers_r_count = data.find_all('div', attrs={'class': 'col-2'})[9].text.replace(' ', '').replace('\n', '')
    
    if len(data.find_all('div', attrs={'class': 'col-2'})[8]) == 4:
        first_blood_r = 1
    else:
        first_blood_r = 0
    
    if len(data.find_all('div', attrs={'class': 'col-2'})[9]) == 4:
        first_tower_r = 1
    else:
        first_tower_r = 0
    
    dragons_r_count = data.find_all('div', attrs={'class': 'col-2'})[10].text.replace(' ', '').replace('\n', '')
    barons_r_count = data.find_all('div', attrs={'class': 'col-2'})[11].text.replace(' ', '').replace('\n', '')
    gold_r_count = data.find_all('div', attrs={'class': 'col-2'})[12].text.replace(' ', '').replace('\n', '')
    
    bans_r_team = []
    for i in range(5):
        bans_r_team.append(data.find_all('div', attrs={'class': 'col-10'})[2].find_all('a')[i].get('title').split()[0])
    
    picks_r_team = []
    for i in range(5):
        picks_r_team.append(data.find_all('div', attrs={'class': 'col-10'})[3].find_all('a')[i].get('title').split()[0])
    
    index = ['Name', 'Result', 'Kills', 'First_Blood', 'Towers', 'First_Tower', 'Dragons', 'Barons', 'Gold', 'Bans', 'Picks', 'Match_id', 'Match_count']
    right_team_stats = pd.Series([r_team_name, r_team_result, kills_r_count, first_blood_r, towers_r_count, first_tower_r, dragons_r_count, barons_r_count, gold_r_count, bans_r_team, picks_r_team, match_id, match_count_i], index=index)
        
    return right_team_stats


def get_players_stats(data: bs4.element.Tag, match_id: int, left_team_picks: list, right_team_picks: list, match_count_i: int) -> pd.DataFrame:

    player_stats_l = data.find_all('tbody')[0].find_all('td')
    nickname_l_team = []
    kda_l_team = []
    cs_l_team = []

    for i in range(0 , len(player_stats_l), 13):
        nickname_l_team.append(player_stats_l[i].text.replace('\n', '').split())

    for i in range(11 , len(player_stats_l), 13):
        kda_l_team.append(player_stats_l[i].text.replace('\n', '').split())

    for i in range(12 , len(player_stats_l), 13):
        cs_l_team.append(player_stats_l[i].text.replace('\n', '').split())
        
    player_stats_r = data.find_all('tbody')[0].find_all('td')
    nickname_r_team = []
    kda_r_team = []
    cs_r_team = []

    for i in range(0 , len(player_stats_r), 13):
        nickname_r_team.append(player_stats_r[i].text.replace('\n', '').split())

    for i in range(11 , len(player_stats_r), 13):
        kda_r_team.append(player_stats_r[i].text.replace('\n', '').split())

    for i in range(12 , len(player_stats_r), 13):
        cs_r_team.append(player_stats_r[i].text.replace('\n', '').split())

        
    gold_distribution = data.find_all('table', attrs={'class': 'small_table'})[0].find_all('td')
    gold_distribution_l_team = []
    gold_distribution_r_team = []
    for i in range(4, len(gold_distribution), 3):
        gold_distribution_l_team.append(gold_distribution[i].text)

    for i in range(5, len(gold_distribution), 3):
        gold_distribution_r_team.append(gold_distribution[i].text)
        
    damage_distribution = data.find_all('table', attrs={'class': 'small_table'})[1].find_all('td')
    damage_distribution_l_team = []
    damage_distribution_r_team = []
    for i in range(4, len(damage_distribution), 3):
        damage_distribution_l_team.append(damage_distribution[i].text)

    for i in range(5, len(damage_distribution), 3):
        damage_distribution_r_team.append(damage_distribution[i].text)
    
    position = ['Top', 'Jungle', 'Mid', 'Adc', 'Support']
    match_id = [match_id, match_id, match_id, match_id, match_id]
    match_count = [match_count_i, match_count_i, match_count_i, match_count_i, match_count_i]
    
    player_stats_l = pd.DataFrame([nickname_l_team, kda_l_team, cs_l_team, damage_distribution_l_team, gold_distribution_l_team, left_team_picks, position, match_id, match_count]).T
    player_stats_r = pd.DataFrame([nickname_r_team, kda_r_team, cs_r_team, damage_distribution_r_team, gold_distribution_r_team, right_team_picks, position, match_id, match_count]).T
    
    return pd.concat([player_stats_l, player_stats_r], ignore_index=True)
