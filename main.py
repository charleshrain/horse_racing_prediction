from RaceInfoScraper import RaceInfoScraper
from DatabaseDownloader import Downloader
from DatabaseImporter import DatabaseImporter
from webscraper import WebScraper
from RandomForest import RandomForest
import sys
import pandas as pd
import html5lib
sys.path.append(".")

def main():
    
    print("Calculate probable winners of upcoming Swedish trotting v75 races\n")

    try: 
        while True:
            print("\nMAIN MENU")
            print("1. Download database Docker file")
            # print("2. Import historical race data to database")
            print("2. Scrape upcoming race data")
            print("3. Scrape upcoming race types")
            print("4. Run Random Forest model")
            print("5. Exit")

            choice1 = int(input("Enter your Choice: "))

            if choice1 == 1:
                print("download docker image")
            elif choice1 == 2:
                upcoming = WebScraper.scrape_race_data()
            
            elif choice1 == 3:
                races = RaceInfoScraper.scrape_race_info()
                
            elif choice1 == 4:
                ret = RandomForest.rforest(races, upcoming)
                pd.set_option('display.max_rows', None)
                print(ret)

            elif choice1 == 5:
                break

            else:
                print("Incorrect Choice.")

    except Exception as e:
      print("An error occured!")
      print(e)
            
if __name__ == "__main__":
        main()

