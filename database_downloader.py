"""Utility module for downloading historical data"""

import shutil

import os

import gzip
import requests



class Downloader:
    """Class for downloading historical data as zipped sql dump"""
    def clean_downloads(self):
        """Remove old downloads"""
        print("Cleaning...\n")

        if os.path.exists('dump.sql'):
            os.remove('dump.sql')
        else:
            print("No such file")

    def download_s3_csv(self):
        """Download file"""
        print("Downloading...\n")
        try:
            url = "https://trottingproject.s3.ca-central-1.amazonaws.com/dump.sql.gz"
            req = requests.get(url, timeout=600)

            with open("dump.sql.gz", 'wb') as file:
                file.write(req.content)
        except Exception as exc:
            print("An error occurred!")
            print(exc)

    def extract_zip(self):
        """Extract downloads and cleanup zip files"""
        zip_file = "dump.sql.gz"
        print("Extracting...\n")

        with gzip.open(zip_file, 'rb') as s_file, \
                open("dump.sql", 'wb') as d_file:
            shutil.copyfileobj(s_file, d_file, 1024)

        if os.path.exists('./dump.sql.gz'):
            os.remove('./dump.sql.gz')
        else:
            print("No such file")
