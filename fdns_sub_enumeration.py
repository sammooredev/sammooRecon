import subprocess
import json
import gzip
import time

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
    time.wait(3)
    print("starting greps, and things. creating final output...")
    

datasetParser('2020-02-28-1582856436-fdns_aaaa.json.gz', 'google.com')