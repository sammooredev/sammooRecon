import threading
import requests
import re
import os
import glob
import multiprocessing
import math
import time
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#for line in alive hosts
    #for line in payloads.txt
        #append payload to host, add line to for_testing.txt

#for line in endpoints
    #replace =http with =https://www.google.com, append to for_testing.txt


#for line in for_testing:
    #send req, follow redirs, if final resp's start = google.com, add to results.txt



def textFormatter(alive_hosts, gau_endpoints, output_path):
    with open(alive_hosts, 'r') as domains: 
        #append hosts + payloads.txt
        for domain in domains:        
            with open('Redirect_Payloads.txt') as payloads:
                for payload in payloads:
                    with open(output_path + 'for_testing.txt', 'a') as results:
                        results.write(domain.strip() + payload)

    #fix up gau endpoints, and add to for_testing.txt 
    with open(gau_endpoints, 'r') as endpoints:
        for line in endpoints:
            url_morphed = re.sub('=http.*?&', '=https://www.google.com', str(line), flags=re.DOTALL)
            final_url = re.sub('=https.*?\n', '=https://www.google.com', str(url_morphed), flags=re.DOTALL)
            with open(output_path + '/for_testing.txt', 'a') as results:
                results.write(final_url + '\n')
    
    #split into 10 files 
def fileSplit():
    os.system('split -l 15000 /root/openredirTest/for_testing.txt /root/openredirTest/tmp/split')


    #multiprocess for files
def worker(file_split, output_path):
    
    print("working on: " + file_split)

    with open(file_split, 'r') as working_file_split:
        for line in working_file_split: 
            try:
                response = requests.get(line, allow_redirects=True, timeout=10, verify=False)
                if response.history:
                    if "www.google.com" in response.url[0:30]:
                        with open(output_path + 'results.txt', 'a') as results:
                            print(str(line) + " -> Redirected to: -> " + str(response.url) + '\n')
                            results.write(str(line) + " -> Redirected to: -> " + str(response.url) + '\n')
            except requests.exceptions.RequestException as e:
                pass        
    print(file_split + " - scan completed")

def main(alive_sites, gau_endpoints, output_path):
    print("formatting files...")
    textFormatter(alive_sites, gau_endpoints, output_path)
    print("splitting files")
    fileSplit()

    threads = []
    for filepath in glob.iglob('/root/openredirTest/tmp/split*'):
        # Create each thread, passing it its chunk of numbers to factor
        # and output dict.
        t = threading.Thread(target=worker,args=(filepath, output_path))
        threads.append(t)
        t.start() 
    

