import os
import urllib3
import zipfile
import os
import http
import requests
import gzip
import zipfile
import shutil

class Downloader:
              
    @classmethod 
    def clean_downloads(cls):
        print("Cleaning...\n")
        if os.path.exists('dump.sql.gz'):
            os.remove('dump.sql.gz')
        
        if os.path.exists('dump.sql'):
            os.remove('dump.sql')

    @classmethod 
    def download_s3_csv(cls):
        print("Downloading...\n")
        try:
            url = "https://trottingproject.s3.ca-central-1.amazonaws.com/dump.sql.gz"
            r = requests.get(url)

            with open("dump.sql.gz",'wb') as f:
                f.write(r.content)        
        except:
            print("An error occured when downloading")

    
    @classmethod
    def extract_zip(cls):
    
        zip_file = "dump.sql.gz"
 
        with gzip.open(zip_file, 'rb') as s_file, \
                open("dump.sql", 'wb') as d_file:
            shutil.copyfileobj(s_file, d_file, 1024)

                