import subprocess
import requests
import gzip
import shutil
import json

#scrape new name of most recent release from https://opendata.rapid7.com/sonar.fdns_v2/, if name matches previously downloaded file, dont download, skip step. 

#rapid7page = 'https://opendata.rapid7.com/sonar.fdns_v2/'
#def GetMostRecentRelease(foo):


    

#download *-fdns.txt.json.gz, unzip it, parse for subdomains!

#download fdns file
#fndsDownloadUrl = 'https://opendata.rapid7.com/sonar.fdns_v2/2020-02-29-1582939737-fdns_txt.json.gz'
#r = requests.get(fndsDownloadUrl)
#open('fdns_txt.json.gz', 'wb').write(r.content)

outputFile = open('output.txt', 'a')

def datasetParser(domain):
    #unzip fdns
    with gzip.GzipFile('testing.txt.gz', 'r') as fin:
        json_bytes = fin.read()
    print("debug 0")
    json_str = json_bytes.decode('utf-8')
    print("debug foo")
    data = json.loads(json_str)
    print("debug 1")
    print(data)
    print("done unzipping... ")
    print("starting greps, and things.")
    grep = subprocess.Popen(['grep', '-F', '.' + str(domain) + '"', 'fdns_txt.json'], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)
    while True:
        output = grep.stdout.readline()
        outputFile.write(output)
        print(output.strip())
        return_code = grep.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output 
            for output in grep.stdout.readlines():
                print(output.strip())
            break
    
datasetParser('google.com')


