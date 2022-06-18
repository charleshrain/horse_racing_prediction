from filecmp import clear_cache
from multiprocessing.connection import wait
import pandas as pd
from prometheus_client import Counter
from selenium import webdriver
from sqlalchemy import false, null
from webdriver_manager.chrome import ChromeDriverManager
import lxml
import time
import numpy as np
from selenium.webdriver.chrome.options import Options
import pandas as pd


class WebScraper:

    counter = 1

    @classmethod
    def inc_couter():
        WebScraper.counter = WebScraper + 1
        return WebScraper.Counter -1
    
    @classmethod
    def calc_win_cur(cls, wins_string):
        
        wins_split = wins_string.split('-')
        
        if len(wins_split[0]) == 3:
            if float(wins_split[0][0:2]) == 0:
                return 0
            else:
                return round(100*float(wins_split[0][2])/float(wins_split[0][0:2]))
        elif len(wins_split[0]) == 4:
            if float(wins_split[0][:1]) == 0:
                return 0
            else:
                return round(100*float(wins_split[0][2:])/float(wins_split[0][:1]))
        elif len(wins_split[0]) == 2:
            if float(wins_split[0][0]) == 0:
                return 0
            else:
                return round(100*float(wins_split[0][1:])/float(wins_split[0][0]))
        else:
            return 0
    
    @classmethod
    def scrape_race_data(cls):

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1680,1050")

        driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=options)

        #get driver ranks
        driver.get('https://sportapp.travsport.se/toplists?categoryId=1&typeId=1&list=S&year=2022&licenseType=S&gender=B&homeTrack=S&raceOnTrack=A&typeOfRace=B&sulkyOrMonte=B&breed=B&returnNumberOfEntries=200&onlyYouth=false')
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/button').click()
        driver_ranks = pd.read_html(driver.find_element_by_css_selector("table[class='RegularTable_table__no-uJ']").get_attribute("outerHTML"))
        # print(driver_ranks)


        # get page pertaining to correct race type
        driver.get('https://www.atg.se/spel/V75')
        driver.find_element_by_css_selector('#onetrust-accept-btn-handler').click()  # cookies popup
        driver.refresh()
        driver.maximize_window()
        time.sleep(10)

        # customize stats button
        driver.find_element_by_class_name('css-eugx3a-startlistoptionsview-styles--configButton-Button--buttonComponent').click()

        #clear stats button
        driver.find_element_by_class_name('css-tqseha-Button-styles--root-Button--Button').click()

        #select stats checkboxes
        pengar_chk = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div/div[3]/div/div[1]/ul/li[1]/div/span[1]').click()
        winp_chk = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div/div[3]/div/div[1]/ul/li[2]/div/span[1]').click()
        placep_chk = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div/div[3]/div/div[2]/ul/li[2]/div/span[1]').click()
        points_chk = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div/div[3]/div/div[2]/ul/li[4]/div/span[1]').click()
        starts_cur = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div/div[3]/div/div[2]/ul/li[6]/div/span[1]').click()

        # save button selected stats
        driver.find_element_by_css_selector("button[data-test-id='save-startlist-options']").click()

        # read upcoming 7 races data into dataframe
        upcoming = pd.DataFrame()

        for i in range(1, 8):

            df = pd.read_html(driver.find_element_by_css_selector('table[data-test-id="startlist-race-' + str(i) +'"]').get_attribute("outerHTML"))
                 
            df0 = df[0]
            df0['Lopp'] = i
            df0 = df0[~df0['Kusk'].str.contains("Tillägg")]
            df0['track'] = df0['Lopp'].index + 1
            upcoming = upcoming.append(df0)
            

        # add 'track' column and clean data
        # upcoming = upcoming[~upcoming['Kusk'].str.contains("Tillägg")]
        # upcoming['track'] = upcoming.index+1
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
            lambda x: WebScraper.calc_win_cur(x))    
        upcoming['money'] = [float(str(val).replace(' ','').replace(',','.')) for val in upcoming['money'].values]
        # upcoming['track'] = np.arange(len(upcoming))
        
        
        driver.quit()
        return upcoming
