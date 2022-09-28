import os
import urllib3
import zipfile
import os
import http
import requests
import gzip
import zipfile

class Downloader:
              
    @classmethod 
    def clean_downloads(cls):
        print("Cleaning...\n")
        if os.path.exists('db-docker.gz'):
            os.remove('db-docker.gz')

        if os.path.exists('data/flat.csv'):
            os.remove('docker-trav-image')

    @classmethod 
    def download_s3_csv(cls):
        print("Downloading...\n")
        try:
            url = "https://trottingproject.s3.ca-central-1.amazonaws.com/docker-portgres-trav-container.gz"
            r = requests.get(url)

            with open("data.zip",'wb') as f:
                f.write(r.content)        
        except:
            print("An error occured when downloading")

    
    @classmethod
    def extract_zip(cls):
    
        zip_file = "data.zip"
 
        try:
            with zipfile.ZipFile(zip_file) as z:
                z.extractall()
                print("Finished extracting")
        except:
            print("Invalid file")

                