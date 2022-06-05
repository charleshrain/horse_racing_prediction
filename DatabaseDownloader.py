

import os

import urllib3

import zipfile

import os

import http

import requests


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
            url = "https://trottingproject.s3.ca-central-1.amazonaws.com/flat.zip"
            r = requests.get(url)

            with open("flat.zip",'wb') as f:
                f.write(r.content)        
        except:
            print("An error occured")
        # finally:
        #     r.release_conn()
    
    @classmethod
    def extract_zip(cls):
        
            with zipfile.ZipFile("flat.zip", 'r') as zip_ref:
                print("Extracting...\n")
                zip_ref.extractall("./data/")

                