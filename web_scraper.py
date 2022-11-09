"""Webscraper for race participant data"""
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager


class WebScraper:
    """Web scraper class"""
    Counter = 1

    def inc_couter(self):
        """Increments counter variable"""
        WebScraper.counter = WebScraper.Counter + 1
        return WebScraper.Counter - 1

    def calc_win_cur(self, wins_string):
        """calculate win percentage in current year"""
        wins_split = wins_string.split('-')

        if len(wins_split[0]) == 3:
            if float(wins_split[0][0:2]) != 0:
                return round(100 * float(wins_split[0][2]) / float(wins_split[0][0:2]))
        if len(wins_split[0]) == 4:
            if float(wins_split[0][:1]) != 0:
                return round(100 * float(wins_split[0][2:]) / float(wins_split[0][:1]))
        if len(wins_split[0]) == 2:
            if float(wins_split[0][0]) != 0:
                return round(100 * float(wins_split[0][1:]) / float(wins_split[0][0]))
        return 0

    def scrape_race_data(self):
        """Scrapes data"""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1680,1050")

        driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=options)

        # get driver ranks
        driver.get(
            'https://sportapp.travsport.se/toplists?categoryId=1&typeId=1&list=S&year=2022&licenseType=S&gender=B&homeTrack=S&raceOnTrack=A&typeOfRace=B&sulkyOrMonte=B&breed=B&returnNumberOfEntries=200&onlyYouth=false')
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/button').click()
        # get page pertaining to correct race type
        driver.get('https://www.atg.se/spel/V75')
        driver.find_element_by_css_selector('#onetrust-accept-btn-handler').click()  # cookies popup
        driver.refresh()
        driver.maximize_window()
        time.sleep(10)

        # customize stats button
        driver.find_element_by_xpath(
            '//*[@id="main"]/div[3]/div[2]/div/div/div/div/div/div/div[5]/div[1]/div[1]/div/div/div/div[2]/div/button[3]').click()

        # clear stats button
        driver.find_element_by_class_name('css-tqseha-Button-styles--root-Button--Button').click()

        # select stats checkboxes
        driver.find_element_by_xpath(
            '/html/body/div[4]/div/div/div/div/div/div[3]/div/div[1]/ul/li[1]/div/span[1]').click()
        driver.find_element_by_xpath(
            '/html/body/div[4]/div/div/div/div/div/div[3]/div/div[1]/ul/li[2]/div/span[1]').click()
        driver.find_element_by_xpath(
            '/html/body/div[4]/div/div/div/div/div/div[3]/div/div[2]/ul/li[2]/div/span[1]').click()
        driver.find_element_by_xpath(
            '/html/body/div[4]/div/div/div/div/div/div[3]/div/div[2]/ul/li[4]/div/span[1]').click()
        driver.find_element_by_xpath(
            '/html/body/div[4]/div/div/div/div/div/div[3]/div/div[2]/ul/li[6]/div/span[1]').click()

        # save button selected stats
        driver.find_element_by_css_selector("button[data-test-id='save-startlist-options']").click()

        # read upcoming 7 races data into dataframe
        upcoming = pd.DataFrame()

        driver.find_element_by_xpath(
            """//*[@id="main"]/div[3]/div[2]/div/div/div/div/div/div/div[5]/div[1]/div[1]/div/div/div/div[2]/div/button[2]""").click()
        driver.find_element_by_xpath(
            """//*[@id="main"]/div[3]/div[2]/div/div/div/div/div/div/div[5]/div[1]/div[1]/div/div/div/div[2]/div/button[2]""").click()

        for i in range(1, 8):

            path = f"(//table[@data-test-id='startlist-race-{i}'])"
            df0 = pd.read_html(driver.find_element_by_xpath(path).get_attribute("outerHTML"))[0]
            df0['Lopp'] = i
            if 'Ryttare' in df0.columns:
                df0.rename(columns={'Ryttare': 'Kusk'}, inplace=True)
            df0 = df0[~df0['Kusk'].str.contains('Tillägg')]
            df0['track'] = df0['Lopp'].index + 1
            upcoming_temp = pd.concat([upcoming, df0])
            upcoming = upcoming_temp

        upcoming.drop(upcoming.columns[[0, 1, 8]], axis=1, inplace=True)

        upcoming.columns = ['betp', 'money',
                            'winp', 'placep', 'points', 'wincur', 'race', 'track']

        upcoming['betp'] = upcoming['betp'].map(
            lambda x: x.lstrip('+-').rstrip('%'))
        upcoming['winp'] = upcoming['winp'].map(
            lambda x: x.lstrip('+-').rstrip('%'))
        upcoming['placep'] = upcoming['placep'].map(
            lambda x: x.lstrip('+-').rstrip('%'))
        upcoming['wincur'] = upcoming['wincur'].map(
            lambda x: WebScraper.calc_win_cur(self, x))
        upcoming['money'] = [float(str(val).replace(' ', '').replace(',', '.')) for val in upcoming['money'].values]
        upcoming['points'] = upcoming['points'].fillna(0)  # quick fix

        driver.quit()
        return upcoming
