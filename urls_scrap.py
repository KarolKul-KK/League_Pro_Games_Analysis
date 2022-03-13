from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import pandas as pd

import time
import re


url = "https://gol.gg/esports/home/"
driver = webdriver.Safari()
driver.get(url)

def get_urls(urls: list) -> None:
        
    data = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'html5lib')
    time.sleep(1)
    table = soup.find('table')
    
    
    for td in table.findAll('td', attrs = {'class': 'footable-visible'}):
        for a in td.findAll('a'):
            data.append(a['href'])
    data = data[1:]
    
    for i in range(0, len(data), 12):
        urls.append(data[i])


def main() -> None:

    urls = []
    while True:
        get_urls(urls)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="previous10"]').click()

    else:
        pd.Series(urls).to_csv('data/games_urls.csv')
        