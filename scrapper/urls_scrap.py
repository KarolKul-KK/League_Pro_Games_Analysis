import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import pandas as pd

import time
import re
import os


def safari_driver() -> selenium.webdriver.safari.webdriver.WebDriver:

    url = "https://gol.gg/esports/home/"
    driver = webdriver.Safari()
    driver.get(url)

    return driver


def make_dir():

    directory = "data"
    os.makedirs(directory, exist_ok=True)
    print("Directory '%s' created or already exist" % directory)


def get_urls(urls: list, driver: selenium.webdriver.safari.webdriver.WebDriver) -> None:

    data = []
    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")
    time.sleep(1)
    table = soup.find("table")

    for td in table.findAll("td", attrs={"class": "footable-visible"}):
        for a in td.findAll("a"):
            data.append(a["href"])
    data = data[1:]

    for i in range(0, len(data), 12):
        urls.append(data[i])


def main() -> None:

    make_dir()
    driver = safari_driver()
    urls = []
    while True:
        get_urls(urls)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="previous10"]').click()

    else:
        pd.Series(urls).to_csv("data/games_urls.csv")

    driver.close()


if __name__ == "__main__":
    main()
