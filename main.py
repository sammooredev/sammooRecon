import os
import time
from commonspeak2_sub_enumeration import CommonSpeakSubGen
from mass_dns_resolution import exec_massdns, awk_sed_sort
from amass_sub_enumeration import amassSpawner
from multiprocessing import Pool

#This is the main file, wrapping the modules. Control flow for this program is: 
#1. run amass, append to amass_potential_subdomains.txt    
#       - run commonspeak2, append to commonspeak2_potential_subdomains.txt
#TO-DO: - run fdns-enum, append to fdns_potential_subdomains.txt
#3. merge amass_potential_subdomains, commonspeak2_potential_subdomains, and fdns_potential_subdomains to one file, potential_subdomains.txt
#2. run massdns on potential_subdomains.txt, output hosts_online_unsorted.txt, sort them, output hosts_online.txt, delete hosts_online_unsorted.txt
#3. run altdns on hosts_online.txt output altdns_potential_subdomains.txt
#4. run massdns on altdns_potential_subdomains, output to altdnsfound_online_unsorted.txt, sort, append to hosts_online.txt 
#5. enumeration finished.

processes = ('amass_sub_enumeration.py', 'commonspeak2_sub_enumeration.py')

def run_process(process):
    os.system('python3 {}'.format(process))

pool = Pool(processes=2)
pool.map(run_process, processes)

os.system("sort -u amass_potential_subdomains.txt commonspeak2_potential_subdomains.txt > all_potential_subdomains.txt")
time.sleep(10)

print("\nstarting massdns resolution...\n")

exec_massdns()
time.sleep(10)
print("DNS Resolution complete, sorting output...")
awk_sed_sort()
print("Subdomain Enumeration Complete! final list: hosts_online.txt")