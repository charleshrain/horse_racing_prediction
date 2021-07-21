import subprocess
from typing_extensions import Concatenate
import urllib3

http = urllib3.PoolManager()
r = http.request('GET', "http://www.travstat.se/travdata2002-2020.zip", preload_content=False)

with open("trav.zip", 'wb') as out:
    while True:
        data = r.read(512)
        if not data:
            break
        out.write(data)

r.release_conn()


import zipfile
with zipfile.ZipFile("./trav.zip", 'r') as zip_ref:
    zip_ref.extractall("./data/")

with zipfile.ZipFile("./data/travdata2002.zip", 'r') as zip_ref:
    zip_ref.extractall("./data/")


# # Copy postgres scripts into folder before running

# delete uneeded files
import os

prefix = ["lopp.", "tvl.", "prog.", "klass.", "variab." ]

for file in os.listdir('./data/'):
    if not file.startswith(tuple(prefix)):
        filename = "./data/" + file
        os.remove(filename)
     

# # check if textfiles are utf-8, if not: use iconv to convert (for loop over .txt files in dir)
# for f in $DIR/racedata/*
# do
#         iconv -f ISO-8859-1 -t UTF-8 "$f" >  "${f%.txt}.utf" 
# done


for file in os.listdir('./data/'):
    file = "./data/" + file
    with open(file, 'r', encoding='ISO-8859-1') as f:
        text = f.read()

    with open(file, 'w', encoding='utf8') as f:
        f.write(text)




# rm $DIR/racedata/*.txt

# for i in $DIR/racedata/*
# do
#     sed 's/\\N/NULL/g' "$i" > "${i%.utf}.txt"
#     # use tr -D "\\N"
# done

# rm $DIR/racedata/*.utf

# echo done

# # create tables in postgres
# psql -U postgres -d postgres -a -f ETL.sql 

# # load datafiles into postgres tables
# #psql postgres postgres -c '\copy lopp FROM './racedata/lopp.txt' 'TXT''

# # run postgres script to create flat table and clean variables
# #psql -U postgres -d postgres -a -f create_flat_table.sql 

# #copy flat table to AWS database