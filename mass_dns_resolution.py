import os 

def awk_sed_sort():
    os.system("cat hosts_online_unsorted | awk '{print $1}' | sed 's/.$//' | sort -u > hosts_online.txt")

def exec_massdns():
    RESOLVERS_PATH = "resolvers.txt"
    os.system('/home/sam/massdns/bin/massdns -s 15000 -t A -o S -r ' + RESOLVERS_PATH + ' --flush -w hosts_online_unsorted.txt all_potential_subdomains.txt')