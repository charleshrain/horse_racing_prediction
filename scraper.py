import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import lxml

from selenium.webdriver.chrome.options import Options

# from selenium.webdriver import ActionChains
import pandas as pd

options = Options()
options.headless = True
options.add_argument("--window-size=1680,1050")

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get('https://www.atg.se/spel/V75')  # get page pertaining to correct race type

driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()  # cookies popup

driver.refresh()

driver.maximize_window()

driver.find_element_by_xpath(
    '//*[@id="main"]/div[3]/div[2]/div/div/div/div/div/div[2]/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/button[2]').click()  # customize race display info

for i in [1, 2, 3, 8, 13]:
    link = '/html/body/div[6]/div/div/div/div/div/div[2]/div/div[1]/ul/li[' + str(
        i) + ']/div/span[1]'  # race info checkboxes
    driver.find_element_by_xpath(link).click()

for i in [1, 2, 4, 6, 7 ]:
    link = '/html/body/div[6]/div/div/div/div/div/div[2]/div/div[2]/ul/li[' + str(
        i) + ']/div/span[1]'  # race info checkboxes

    driver.find_element_by_xpath(link).click()

driver.find_element_by_xpath(
    '/html/body/div[6]/div/div/div/div/div/div[2]/div/div[3]/button[2]').click()  # save custom display info

# df = pd.read_html(driver.find_element_by_class_name('game-table').get_attribute("outerHTML"))

upcoming = pd.DataFrame()

for i in range(1,7):

    df = pd.read_html(driver.find_element_by_xpath('//*[@id="main"]/div[3]/div[2]/div/div/div/div/div/div[2]/div[6]/div[' + str(i) +']/div/div/table').get_attribute("outerHTML"))

    df0 = df[0]
    df0['Lopp'] = i
    upcoming = upcoming.append(df[0])


# driver.quit()

