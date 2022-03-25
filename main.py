import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from game_stats_scrapper import get_match_count,  get_general_data, get_left_team_stats, get_right_team_stats, get_players_stats
from urls_scrap import make_dir

import time
import random


def main() -> None:

    general_table = pd.DataFrame()
    left_team_stats_table = pd.DataFrame()
    right_team_stats_table = pd.DataFrame()
    players_stats_table = pd.DataFrame()
    driver = webdriver.Safari()
    make_dir()
    urls_table = pd.read_csv('data/Matches_urls.csv')
    urls = urls_table['matches_urls'].drop_duplicates().reset_index()['matches_urls']

    for url in urls:
        active_url = f'https://gol.gg{url[2:]}'
        driver.get(active_url)

        time.sleep(random.randint(2, 4))

        html = driver.page_source
        soup = BeautifulSoup(html, 'html5lib')

        match_count, data = get_match_count(soup)

        for i in range(match_count):
            general_data_series = get_general_data(data, active_url)
            left_team_stats = get_left_team_stats(data)
            right_team_stats = get_right_team_stats(data)
            player_stats = get_players_stats(data)

            general_table = pd.concat([general_table, general_data_series], ignore_index=True)
            left_team_stats_table = pd.concat([left_team_stats_table, left_team_stats], ignore_index=True)
            right_team_stats_table = pd.concat([right_team_stats_table, right_team_stats], ignore_index=True)
            players_stats_table = pd.concat([players_stats_table, player_stats])


if __name__ == "__main__":
    main()


        

        
