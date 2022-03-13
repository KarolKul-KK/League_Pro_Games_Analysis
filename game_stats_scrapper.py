from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import pandas as pd

import time
import re


def get_match_count() -> int:
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html5lib')
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
        
    return int(match_count)


def get_general_data() -> str:
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html5lib')
    
    pattern = '\d{1,}'
    result = re.search(pattern, active_url)
    match_id = result.group(0)
    
    data = soup.find_all('div')[16]
    
    match_date = data.find('div', attrs={'class': 'col-12 col-sm-5 text-right'}).text
    team_names = data.find('h1').text.split('vs')
    tournament_name = data.find('a').text
    game_time = data.find('div', attrs={'class': 'col-6 text-center'}).find('h1').text
    
    return match_id, match_date, team_names[0], team_names[1], tournament_name, game_time


def get_left_team_stats() -> str:
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html5lib')
    data = soup.find_all('div')[16]
    
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

    return l_team_result, kills_l_counts, first_blood_l, towers_l_count, first_tower_l, dragons_l_count, baron_l_count, gold_l_count, bans_l_team, picks_l_team 

