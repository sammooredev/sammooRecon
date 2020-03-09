import subprocess
import json
import gzip
import time
import requests
import urllib.request
import glob
from bs4 import BeautifulSoup



def checkNeed():
    #fetch most recent fdns file name.
    soup = BeautifulSoup(requests.get("https://opendata.rapid7.com/sonar.fdns_v2/").text, "lxml")
    for x in soup.find_all('a',attrs={"rel":"nofollow"}):
        if "37-fdns_txt" in x["href"]:
            newfdnsFileName = x["href"].replace('sonar.fdns_v2/','')


    #fetch owned fdns file name.
    path = "*.json.gz"
    for filename in glob.glob(path):
        owned_fdns_file = filename or "none"
    #compare fetched fdns file name against owned fdns file.
    if newfdnsFileName == owned_fdns_file:
        print("You already own this dataset! Skipping download, moving on.")

    else:
        print("These fuckers are not the same, you need a new dataset! Going to download the new FDNS dataset, brb...")
        downloadUrl = 'https://opendata.rapid7.com/sonar.fdns_v2' + newfdnsFileName
        print(downloadUrl)
        local_filename = downloadUrl.split('/')[-1]
        print(local_filename)
        with requests.get(downloadUrl, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        f.flush()
        print(local_filename)
checkNeed()

def datasetParser(fdnsfile, domain):
    #unzip fdns
    outputFile = open("fdns_potential_subdomains.txt", "a")
    print("opened output file")
    with gzip.open(fdnsfile, 'r') as fin:
        print("opened folder to unzip")
        for line in fin:
            if domain.encode() in line:
                outputFile.write(str(json.loads(line)))
                #json_bytes = fin.read()
                #json_str = json_bytes.decode('utf-8')
                #data = json.loads(json_str)
    #print(data)
    print("done parsing file! ")
    time.sleep(3)
    print("starting greps, and things. creating final output...")
    

#datasetParser('2020-02-28-1582856436-fdns_aaaa.json.gz', 'google.com')