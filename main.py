""""Program to forecast probability of winning in future horse races"""
import sys
import sqlalchemy as db
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import database_downloader
import race_scraper
import random_forest
import web_scraper
import time

sys.path.append(".")


def main():
    """"Main program"""
    print("Calculate probable winners of upcoming Swedish trotting v75 races\n")

    races = None
    upcoming = None

    options = Options()
    options.add_argument("--window-size=1680,1050")
    options.add_argument("--headless")

    with webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options) as driver:
        driver.get("chrome://settings/clearBrowserData")
        time.sleep(5)
        driver.switch_to.active_element
        driver.get('https://www.atg.se/spel/V75')
        driver.find_element_by_css_selector('#onetrust-accept-btn-handler').click()  # accept cookies
        driver.refresh()

        engine = db.create_engine('postgresql://postgres:postgres@localhost:5432/trav')
        connection = engine.connect()

        while True:
            print("\nMAIN MENU")
            print("1. Download database Docker file")
            print("2. Scrape upcoming race data")
            print("3. Scrape upcoming race types")
            print("4. Run Random Forest model")
            print("5. Exit")

            choice1 = int(input("Enter your Choice: "))

            if choice1 == 1:
                downloader = database_downloader.Downloader()
                downloader.clean_downloads()
                downloader.download_s3_csv()
                downloader.extract_zip()
            elif choice1 == 2:
                w_scraper = web_scraper.WebScraper(driver)
                upcoming = w_scraper.scrape_race_data()
            elif choice1 == 3:
                my_race = race_scraper.RaceInfoScraper(driver)
                races = my_race.scrape_race_info()
            elif choice1 == 4:
                runner = random_forest.RandomForestRunner(connection)
                ret = runner.rforest(races, upcoming)
                pd.set_option('display.max_rows', None)
                print(ret)

            elif choice1 == 5:
                break

            else:
                print("Incorrect Choice.")


if __name__ == "__main__":
    main()
