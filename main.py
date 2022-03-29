import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from game_stats_scrapper import get_match_count,  get_general_data, get_left_team_stats, get_right_team_stats, get_players_stats, make_dir

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
            time.sleep(3)
            general_data_series = get_general_data(data, active_url)
            time.sleep(1)
            left_team_stats = get_left_team_stats(data, general_data_series['Match_id'], i)
            time.sleep(1)
            right_team_stats = get_right_team_stats(data, general_data_series['Match_id'], i)
            time.sleep(1)
            player_stats = get_players_stats(data, general_data_series['Match_id'], left_team_stats['Picks'], right_team_stats['Picks'], i)
            time.sleep(1)
            print(general_data_series['Date'])

            general_table = pd.concat([general_table, pd.DataFrame(general_data_series).T], ignore_index=True)
            left_team_stats_table = pd.concat([left_team_stats_table, pd.DataFrame(left_team_stats).T], ignore_index=True)
            right_team_stats_table = pd.concat([right_team_stats_table, pd.DataFrame(right_team_stats).T], ignore_index=True)
            players_stats_table = pd.concat([players_stats_table, player_stats], ignore_index=True)

            driver.find_element_by_xpath(f'//*[@id="gameMenuToggler"]/ul/li[{i+3}]/a').click()

    general_table.to_csv('data/general_data.csv')
    pd.concat([left_team_stats, right_team_stats], ignore_index=True).to_csv('data/team_stats.csv')
    players_stats_table.to_csv('data/players_stats.csv')


if __name__ == "__main__":
    main()


        

        
