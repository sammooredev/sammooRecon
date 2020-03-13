import os 

def awk_sed_sort():
    os.system("cat hosts_online_unsorted.txt | awk '{print $1}' | sed 's/.$//' | sort -u > hosts_online.txt")

def exec_massdns():
    RESOLVERS_PATH = "resolvers.txt"
    os.system('/home/sam/massdns/bin/massdns -s 15000 -t A -o S -r ' + RESOLVERS_PATH + ' --flush -w /online_hosts/hosts_online_unsorted.txt /potential_subdomains/all_potential_subdomains.txt')