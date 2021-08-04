from racewebscraper import racescraper
from dbdownloader import downloader
from dbetl import dbimport
from webscraper import webscraper
from forest import forest
import sys
import pandas as pd
sys.path.append(".")

def main():
    

    print("Calculate probability of winning\n")

    while True:
        print("\nMAIN MENU")
        print("1. Download data")
        print("2. Import data to database")
        print("3. webscrape")
        print("4. racescrape")
        print("5. Forest")
        print("6. Exit")

        
        
        try: 
            choice1 = int(input("Enter the Choice: "))
        except ValueError:
            print("That's not an int!")
            continue

        if choice1 == 1:
            downloader.cleanup()
            downloader.s3_download()
            downloader.extract_zip()

        elif choice1 == 2:
            try:
                dbimport.import_data()
            except:
                print("No databas connected")
        elif choice1 == 3:
            upcoming = webscraper.scrape()
        
        elif choice1 == 4:
            races = racescraper.racescrape()
            
        elif choice1 == 5:
            ret = forest.rforest(races, upcoming)
            pd.set_option('display.max_rows', None)
            print(ret)

        elif choice1 == 6:
            break

        else:
            print("Oops! Incorrect Choice.")
            
if __name__ == "__main__":
        main()

