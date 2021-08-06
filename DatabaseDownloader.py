

import os

import urllib3

import zipfile

import os

import http


class Downloader:
    
    name = None
    age = None
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
          
    @classmethod 
    def clean_downloads(cls):
        print("Cleaning...\n")
        if os.path.exists('flat.zip'):
            os.remove('flat.zip')

        if os.path.exists('data/flat.csv'):
            os.remove('data/flat.csv')

    @classmethod 
    def download_s3_csv(cls):
        print("Downloading...\n")
        try:
            http = urllib3.PoolManager()
            r = http.request(
                'GET', "https://trottingproject.s3.ca-central-1.amazonaws.com/flat.zip", preload_content=False)

            with open("flat.zip", 'wb') as out:
                while True:
                    data = r.read(512)
                    if not data:
                        break
                    out.write(data)
        except:
            print("An error occured")
        finally:
            r.release_conn()
    
    @classmethod
    def extract_zip(cls):
        
            with zipfile.ZipFile("flat.zip", 'r') as zip_ref:
                print("Extracting...\n")
                zip_ref.extractall("./data/")

                