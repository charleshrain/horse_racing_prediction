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

    while True:
        print("\nMAIN MENU")
        print("1. Download historical race data")
        print("2. Import historical race data to database")
        print("3. Scrape upcoming race data")
        print("4. Scrape upcoming race types")
        print("5. Run Random Forest model")
        print("6. Exit")

        
        
        try: 
            choice1 = int(input("Enter your Choice: "))
        except ValueError:
            print("That's not a valid number!")
            continue

        if choice1 == 1:
            Downloader.clean_downloads()
            Downloader.download_s3_csv()
            Downloader.extract_zip()

        elif choice1 == 2:
            try:
                DatabaseImporter.import_db_data()
            except:
                print("No database connected")
        elif choice1 == 3:
            upcoming = WebScraper.scrape_race_data()
        
        elif choice1 == 4:
            races = RaceInfoScraper.scrape_race_info()
            
        elif choice1 == 5:
            ret = RandomForest.rforest(races, upcoming)
            pd.set_option('display.max_rows', None)
            print(ret)

        elif choice1 == 6:
            break

        else:
            print("Incorrect Choice.")
            
if __name__ == "__main__":
        main()

