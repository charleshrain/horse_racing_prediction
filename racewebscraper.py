import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import lxml
from selenium.webdriver.chrome.options import Options
import pandas as pd

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1680,1050")

driver = webdriver.Chrome(
    ChromeDriverManager().install(), chrome_options=options)

driver.get('https://www.atg.se/spel/V75')
driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
driver.refresh()
driver.maximize_window()


def decide_class(data):

    data = str(data).lower().replace(" ", "")

    classes = {'bronsdivisionen': 'B',
               'dubbelklasslopp': 'D',
               'elitlopp': 'E',
               'flerklasslopp': 'F',
               'gulddivisionen': 'G',
               'kallblodslopp': 'K',
               'klass1': '1',
               'klass2': '2',
               'rlingslopp': 'L',
               'silverdivisionen': 'S',
               'stodivisionen': 'Q',
               'stoeliten': 'X',
               'utomv5': 'U',
               'Vv5lopp': 'V'}

    for classkey, symbol in classes.items():
        if classkey in data:
            return symbol


def decide_distance(data):

    data = str(data).lower().replace(" ", "")

    distances = {'1650': 'K',
                 '1609': 'K',
                 '2100': 'M',
                 '2140': 'M',
                 '2175': 'M',
                 '2300': 'M',
                 '2550': 'L',
                 '2609': 'L',
                 '2640': 'L',
                 '2700': 'S',
                 '2850': 'S',
                 '3140': 'S',
                 '3160': 'S',
                 '4000': 'S'}

    for distkey, symbol in distances.items():
        if distkey in data:
            return symbol


def decide_startmode(data):
    data = str(data).lower().replace(" ", "")

    startmode = {'autostart': 'A',
                 'voltstart': 'V'}

    for startkey, symbol in startmode.items():
        if startkey in data:
            return symbol


races = pd.DataFrame(columns=['race', 'class', 'distance', 'start'])

for i in range(1, 8):
    print(i)
    klass = decide_class(driver.find_element_by_xpath(
        '//*[@id="main"]/div[3]/div[2]/div/div/div/div/div/div[2]/div[6]/div['+str(i)+']/div/div/div[1]/div/div[1]/div/div[2]/div[1]/span[3]').get_attribute("innerHTML"))
    distans = decide_distance(driver.find_element_by_xpath(
        '//*[@id="main"]/div[3]/div[2]/div/div/div/div/div/div[2]/div[6]/div['+str(i)+']/div/div/div[1]/div/div[1]/div/div[2]/div[2]/div[2]/span').get_attribute("innerHTML"))
    startmode = decide_startmode(driver.find_element_by_xpath(
        '//*[@id="main"]/div[3]/div[2]/div/div/div/div/div/div[2]/div[6]/div['+str(i)+']/div/div/div[1]/div/div[1]/div/div[2]/div[2]/div[2]/span').get_attribute("innerHTML"))
    races.loc[i] = [i, klass, distans, startmode]

driver.quit()

