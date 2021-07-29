from dbdownloader import downloader
import sys
sys.path.append(".")

def main():
    
    

    print("Calculate probability of winning\n")

    while True:
        print("\nMAIN MENU")
        print("1. Download data")
        print("2. Do something")
        print("3. Exit")
        
        
        try: 
            choice1 = int(input("Enter the Choice:"))
        except ValueError:
            print("That's not an int!")
            continue

        if choice1 == 1:
            downloader.cleanup()
            downloader.s3_download()
            downloader.extract_zip()

        elif choice1 == 2:
            print("\nCALCULATE AREA")

        elif choice1 == 3:
            break

        else:
            print("Oops! Incorrect Choice.")
            
if __name__ == "__main__":
        main()

