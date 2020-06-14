import json
import glob
import os
import datetime
import re
from tinydb import TinyDB, Query

# date
grabdate = datetime.datetime.now().date()
date = str(grabdate)

# use to create directories in each path
program_path = "/root/Bounty/*"
# use to work on each domains list of each program
path = "/root/Bounty/*/*/domains.txt"

def fdnsParse(fdnsfile, domain, output_path):
    placeholder = '.'+domain+'"'
    placeholder2 = '.'+domain+'$'
    os.system("zcat " + fdnsfile + " | grep -F '" + placeholder + "' | jq -r .name | grep '" + placeholder2 +
              "' | sort | uniq | tee -a " + output_path + "/potential_subdomains/" + date + "_fdns_potential_subdomains.txt")

def fdnsLookUp(fdnsfile, domain, output_path):
    os.system

def exec_massdns(output_path):
    RESOLVERS_PATH = "resolvers.txt"

    #[5] run massdns
    os.system('/root/massdns/bin/massdns -s 15000 -t A -o S -r ' + RESOLVERS_PATH + ' --flush -w ' + output_path + '/' + date +
              '/online_hosts/hosts_online_unsorted.txt ' + output_path + '/' + date + '/potential_subdomains/' + date + '_all_potential_subdomains.txt')
    # clean output to just be a domain
    os.system("cat " + output_path + "/" + date + 
              "/online_hosts/hosts_online_unsorted.txt | awk '{print $1}' | sed 's/.$//' | sort -u > " + output_path + "/" + date + "/online_hosts/" + date + "_online_hosts.txt")
    os.system('cat ' + output_path + "/" + date + '/online_hosts/hosts_online_unsorted.txt | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" | sort -u > ' + output_path + "/" + date + "/online_hosts/for_masscan_1.txt")
    os.system("rm -f " + output_path + "/" + date + "/online_hosts/hosts_online_unsorted.txt")
    print(" [+] MassDNS done, creating altdns possibilites...")


def exec_massdns_final(output_path):
    RESOLVERS_PATH = "resolvers.txt"
    os.system('/root/massdns/bin/massdns -s 15000 -t A -o S -r ' + RESOLVERS_PATH + " --flush -w " + output_path + "/" + date + 
              "/online_hosts/altdns_online_unsorted_final.txt " + output_path + "/" + date + "/potential_subdomains/" + date + "_altdns_potential_subdomains.txt")

    os.system("cat " + output_path + "/" + date + "/online_hosts/altdns_online_unsorted_final.txt | awk '{print $1}' | sed 's/.$//' | sort -u > " + output_path + "/" + date + "/online_hosts/" + date + "_altdns_online_hosts.txt")
    os.system('cat ' + output_path + "/" + date + '/online_hosts/altdns_online_unsorted_final.txt | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" | sort -u > ' + output_path + '/' + date + '/online_hosts/for_masscan_2.txt') 
    os.system('rm -f ' + output_path + "/" + date + "/online_hosts/altdns_online_unsorted_final.txt") 
    os.system("sort -u " + output_path + "/" + date + "/online_hosts/" + date + "_online_hosts.txt " + output_path + "/" + date +  
              "/online_hosts/" + date + "_altdns_online_hosts.txt > " + output_path + "/" + date + "/online_hosts/final_online_hosts/final_online_hosts.txt")
    os.system("sort -u " + output_path + "/" + date + "/online_hosts/for_masscan_2.txt " + output_path + '/' + date + '/online_hosts/for_masscan_1.txt > ' + output_path + "/" + date + "/online_hosts/for_ping_scan.txt")
    os.system("rm " + output_path + "/" + date + "/online_hosts/for_masscan_2.txt")
    os.system("rm " + output_path + "/" + date + "/online_hosts/for_masscan_1.txt")
    print(" [+] Final MassDNS done.")
# Generate possible subdomains with commonspeak2


def CommonSpeakSubGen(domain, output_path):
    scope = str(domain)
    wordlist = open('./commonspeak2.txt').read().split('\n')
    outputFile = open(str(output_path) + "/" + date + "/potential_subdomains/" +
                      date+"_commonspeak2_potential_subdomains.txt", "w")

    for word in wordlist:
        if not word.strip():
            continue
        outputFile.write('{}.{}\n'.format(word.strip(), scope))
    print("finished CommonSpeak generation for: " + str(domain))


def altDNSer(output_path):
    os.system('altdns -i ' + output_path + '/' + date + '/online_hosts/' + date + '_online_hosts.txt -o ' + output_path + "/" + date +
              "/potential_subdomains/" + date + "_altdns_potential_subdomains.txt -w ../altdns/words.txt")

    print(" [+] altdns generation complete")


for file in glob.glob(program_path):
    
    dir_path = str(file) + "/*"
    for file in glob.glob(dir_path):
        print('making dir at ' + file)
        os.system("mkdir " + file + "/" + str(date))
        os.system("mkdir " + file + "/" + str(date) + "/potential_subdomains")
        os.system("mkdir " + file + "/" + str(date) + "/online_hosts")
        os.system("mkdir " + file + "/" + str(date) + "/online_hosts/final_online_hosts")
        os.system("mkdir " + file + "/" + str(date) + "/online_hosts/final_online_hosts/alive_sites")
        os.system("mkdir " + file + "/" + str(date) + "/online_hosts/final_online_hosts/403s")
        os.system("touch " + file + "/" + str(date) + "/online_hosts/final_online_hosts/database.json")
        #db = TinyDB(file + '/' + date + "/online_hosts/final_online_hosts/database.json")
        #table = db.table(str(file))

        domains_file = str(file) + '/domains.txt'
        print(domains_file)
        print(" [+] starting enum for: " + str(domains_file).replace(
            "home/sam/Bounty/", " == ").replace("/domains.txt", " == "))
        #[1]Run amass on each line of domains.txt
        os.system('/snap/bin/amass enum -timeout 30  -df ' + str(domains_file) + ' | tee -a ' + file + '/' + date + '/potential_subdomains/' + date + '_amass_potential_subdomains.txt')

        #[2]generate commonspeak possibilites
        program = file
        print(program)
        with open(str(domains_file), "r") as domain_list:
            # iterate through domains.txt
            for domain in domain_list:
                # fixed_domain is a line stripped of whitespace/newlines
                fixed_domain = domain.strip()

                # run commonspeak function for each line of domains.txt
                CommonSpeakSubGen(str(fixed_domain), str(program))

                #[3]parse fdns for each line of domains.txt
                fdns_path = "/home/sam/Bounty/*.json.gz"
                for filename in glob.glob(fdns_path):
                    owned_fdns_file = filename or "none"

                # print("Parsing FDNS for: " + domain)
                # fdnsParse(owned_fdns_file, domain, str(file).replace("domains.txt",""))
        #[4]merge all potential subdomains into one file
        os.system("sort -u " + file + '/' + date + "/potential_subdomains/" + date + "_amass_potential_subdomains.txt " + file + "/" + date + "/potential_subdomains/" +
                  date+"_commonspeak2_potential_subdomains.txt > " + file + "/" + date + "/potential_subdomains/" + date + "_all_potential_subdomains.txt")
        exec_massdns(file)
        altDNSer(file)
        exec_massdns_final(file)
        #ffuf non ssl alive domains
        os.system('wc -l < ' + file + '/' + date + '/online_hosts/final_online_hosts/final_online_hosts.txt > ' + file + '/' + date + '/online_hosts/final_online_hosts/number_of_lines.txt')
        with open(file + '/' + date + '/online_hosts/final_online_hosts/number_of_lines.txt') as f:
            numlines = f.readline()
            bad_resp = ['403','302']
            if int(numlines) > 250000:
                os.system('split -l 250000 ' + file + '/' + date + '/online_hosts/final_online_hosts/final_online_hosts.txt ' + file + '/' + date + '/online_hosts/final_online_hosts/xsplit')
                print('spliit!') 

                for kid in glob.glob(file + "/" + date + "/online_hosts/final_online_hosts/xsplit*"):
                    print(kid)

                    os.system('ffuf -c -w "' + kid +':DOMAIN" -w /root/ffuf_blank.txt -u http://DOMAIN/FUZZ -timeout 2 -t 200 -o ' + file + '/' + date + '/online_hosts/final_online_hosts/no_ssl_alive_fuzz.json -of json')
                    with open(file + '/' + date + "/online_hosts/final_online_hosts/no_ssl_alive_fuzz.json") as ffuzjson:
                        data = json.load(ffuzjson)

                        for key in data['results']:
                            if any(resp in str(key['status']) for resp in bad_resp):
                                with open(file + "/" + date + '/online_hosts/final_online_hosts/403s/403_sites.txt', 'a') as g:
                                    g.write(key['url'] + '\n')
                            else:
                                with open(file + "/" + date + '/online_hosts/final_online_hosts/alive_sites/alive_sites.txt', 'a') as h:
                                    h.write(key['url'] + '\n')
        #ffuf ssl alive domains                
                    os.system('ffuf -c -w "' + kid + ':DOMAIN" -w /root/ffuf_blank.txt -u https://DOMAIN/FUZZ -timeout 2 -t 200 -o ' + file + '/' + date + '/online_hosts/final_online_hosts/ssl_alive_fuzz.json -of json')
                    with open(file + '/' + date + "/online_hosts/final_online_hosts/ssl_alive_fuzz.json") as ffuzjson:
                        data = json.load(ffuzjson)

                    for key in data['results']:
                        if any(resp in str(key['status']) for resp in bad_resp): 
                            with open(file + "/" + date + '/online_hosts/final_online_hosts/403s/403_sites.txt', 'a') as g:
                                g.write(key['url'] + '\n')    
                        else:
                            with open(file + "/" + date + '/online_hosts/final_online_hosts/alive_sites/alive_sites.txt', 'a') as h:
                                h.write(key['url'] + '\n')
            else:
                os.system('ffuf -c -w "' + file + '/' + date + '/online_hosts/final_online_hosts/final_online_hosts.txt:DOMAIN" -w /root/ffuf_blank.txt -u http://DOMAIN/FUZZ -timeout 2 -t 200 -o ' + file + '/' + date + '/online_hosts/final_online_hosts/no_ssl_alive_fuzz.json -of json')
                with open(file + '/' + date + "/online_hosts/final_online_hosts/no_ssl_alive_fuzz.json") as ffuzjson:
                    data = json.load(ffuzjson)

                    for key in data['results']:
                        if any(resp in str(key['status']) for resp in bad_resp):
                            with open(file + "/" + date + '/online_hosts/final_online_hosts/403s/403_sites.txt', 'a') as g:
                                g.write(key['url'] + '\n')
                        else:
                            with open(file + "/" + date + '/online_hosts/final_online_hosts/alive_sites/alive_sites.txt', 'a') as h:
                                h.write(key['url'] + '\n')



                os.system('ffuf -c -w "' + file + '/' + date + '/online_hosts/final_online_hosts/final_online_hosts.txt:DOMAIN" -w /root/ffuf_blank.txt -u https://DOMAIN/FUZZ -timeout 2 -t 200 -o ' + file + '/' + date + '/online_hosts/final_online_hosts/no_ssl_alive_fuzz.json -of json')
                with open(file + '/' + date + "/online_hosts/final_online_hosts/no_ssl_alive_fuzz.json") as ffuzjson:
                    data = json.load(ffuzjson)

                    for key in data['results']:
                        if any(resp in str(key['status']) for resp in bad_resp):
                            with open(file + "/" + date + '/online_hosts/final_online_hosts/403s/403_sites.txt', 'a') as g:
                                g.write(key['url'] + '\n')
                        else:
                            with open(file + "/" + date + '/online_hosts/final_online_hosts/alive_sites/alive_sites.txt', 'a') as h:
                                h.write(key['url'] + '\n')

        os.system('rm ' + file + '/' + date + '/online_hosts/final_online_hosts/xsplit*')
        os.system('rm ' + file + '/' + date + '/potential_subdomains/*potential_subdomains.txt')
        os.system('rm '+ file + '/' + date + '/online_hosts/*online_hosts.txt')
        print(" [+] enumeration complete for: " + file)
