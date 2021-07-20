import subprocess


# subprocess.run(["mkdir","-p", "db_download"])
# subprocess.run(["cd", "db_download" ])
# subprocess.run(["wget", "http://www.travstat.se/travdata2002-2020.zip"])
# subprocess.run(["unzip", "*" ])
# subprocess.run(["rm", "*.zip" ])

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



# # Copy postgres scripts into folder before running


# # delete unneeded files
# find ./racedata -type f -not \( -name  "lopp.txt" -o -name "tvl.txt" -o -name "prog.txt" -o -name "klass.txt" -o -name "variab.txt" \) | xargs rm

import os
for filename in os.listdir('dirname'):
     callthecommandhere(blablahbla, filename, foo)

# # check if textfiles are utf-8, if not: use iconv to convert (for loop over .txt files in dir)
# for f in $DIR/racedata/*
# do
#         iconv -f ISO-8859-1 -t UTF-8 "$f" >  "${f%.txt}.utf" 
# done

sourceEncoding = "iso-8859-1"
targetEncoding = "utf-8"
source = open("source")
target = open("target", "w")

target.write(unicode(source.read(), sourceEncoding).encode(targetEncoding))


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