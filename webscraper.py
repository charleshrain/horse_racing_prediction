import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import lxml

from selenium.webdriver.chrome.options import Options

# from selenium.webdriver import ActionChains
import pandas as pd


class WebScraper:
    @classmethod
    def scrape_race_data(cls):

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1680,1050")

        driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=options)

        # get page pertaining to correct race type
        driver.get('https://www.atg.se/spel/V75')
        driver.find_element_by_xpath(
            '//*[@id="onetrust-accept-btn-handler"]').click()  # cookies popup
        driver.refresh()
        driver.maximize_window()
        driver.find_element_by_xpath(
            '//*[@id="main"]/div[3]/div[2]/div/div/div/div/div/div[2]/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/button[2]').click()  # customize race display info

        for i in [1, 2]:
            link = '/html/body/div[4]/div/div/div/div/div/div[2]/div/div[1]/ul/li[' + str(
                i) + ']/div/span[1]'  # race info checkboxes
            driver.find_element_by_xpath(link).click()


        for i in [2, 4]:
            link = '/html/body/div[4]/div/div/div/div/div/div[2]/div/div[2]/ul/li[' + str(
                i) + ']/div/span[1]'  # race info checkboxes

            driver.find_element_by_xpath(link).click()

        driver.find_element_by_xpath(
            '/html/body/div[4]/div/div/div/div/div/div[2]/div/div[3]/button[2]').click()  # save custom display info

        upcoming = pd.DataFrame()

        for i in range(1, 8):

            df = pd.read_html(driver.find_element_by_xpath(
                '//*[@id="main"]/div[3]/div[2]/div/div/div/div/div/div[2]/div[6]/div[' + str(i) + ']/div/div/table').get_attribute("outerHTML"))

            df0 = df[0]
            df0['Lopp'] = i
            upcoming = upcoming.append(df[0])

        upcoming = upcoming[~upcoming['Kusk'].str.contains("Tillägg")]
        upcoming['track'] = upcoming.index+1
        upcoming.drop(upcoming.columns[[0, 1, 7, 8]], axis=1, inplace=True)

        upcoming.columns = ['betp', 'money',
                            'winp', 'placep', 'points', 'race', 'track']

        upcoming['betp'] = upcoming['betp'].map(
            lambda x: x.lstrip('+-').rstrip('%'))
        upcoming['winp'] = upcoming['winp'].map(
            lambda x: x.lstrip('+-').rstrip('%'))
        upcoming['placep'] = upcoming['placep'].map(
            lambda x: x.lstrip('+-').rstrip('%'))
        
        upcoming['money'] = [float(str(val).replace(' ','').replace(',','.')) for val in upcoming['money'].values]
        
        driver.quit()
        return upcoming
