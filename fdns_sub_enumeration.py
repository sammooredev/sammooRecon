import subprocess
import json
import gzip
import time
import requests
import glob
from bs4 import BeautifulSoup


def fetch_FDNS_File():
    soup = BeautifulSoup(requests.get("https://opendata.rapid7.com/sonar.fdns_v2/").text, "lxml")
    for x in soup.find_all('a',attrs={"rel":"nofollow"}):
        if "any" in x["href"]:
            return x["href"]

def checkNeed():
    newfdnsfile = fetch_FDNS_File().replace('/','')
    print(newfdnsfile)
    path = "*.json.gz"
    for filename in glob.glob(path):
        print(filename)

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