import urllib3
import zipfile
import os
import http

try:

    if os.path.exists('v75flat.zip'):
        os.remove('v75flat.zip')

    # if os.path.exists('./data/*'):
    #     os.remove('./data/*')

    http = urllib3.PoolManager()
    r = http.request('GET', "http://trottingproject.s3.amazonaws.com/v75flat.zip", preload_content=False)


    with open("v75flat.zip", 'wb') as out:
        while True:
            data = r.read(512)
            if not data:
                break
            out.write(data)
except:
    print("An error occured") 
finally:
    r.release_conn()



with zipfile.ZipFile("v75flat.zip", 'r') as zip_ref:
    zip_ref.extractall("./data/")


