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

def nslookup_loop(output_path):
    domains_for_ns = open(output_path + "/" + date + "/online_hosts/final_online_hosts/" + date + "_final_online_hosts.txt", "r") 
    for domain in domains_for_ns:
        fixed_domain = domain.strip()
        print("IPs grabbed for: " + fixed_domain)
        grepip = r"([0-9]{1,3}[\.]){3}[0-9]{1,3}"
        foobar = '/Name:/{val=$NF;flag=1;next} /Address:/ && flag{print $NF,val;val=""}'
        os.system('nslookup ' + fixed_domain + ' |  awk ' + "'" + foobar + "'" + ' | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" | sort -u > temp_ns_outfile.txt')
        os.system('cat temp_ns_outfile.txt >> ' + output_path + '/' + date + '/online_hosts/' + date + '_for_masscan.txt')

def fdnsParse(fdnsfile, domain, output_path):
    placeholder = '.'+domain+'"'
    placeholder2 = '.'+domain+'$'
    os.system("zcat " + fdnsfile + " | grep -F '" + placeholder + "' | jq -r .name | grep '" + placeholder2 +
              "' | sort | uniq | tee -a " + output_path + "/potential_subdomains/" + date + "_fdns_potential_subdomains.txt")


def exec_massdns(output_path):
    RESOLVERS_PATH = "resolvers.txt"

    #[5] run massdns
    os.system('/root/massdns/bin/massdns -s 15000 -t A -o S -r ' + RESOLVERS_PATH + ' --flush -w ' + output_path + '/' + date +
              '/online_hosts/hosts_online_unsorted.txt ' + output_path + '/' + date + '/potential_subdomains/' + date + '_all_potential_subdomains.txt')
    # clean output to just be a domain
    os.system("cat " + output_path + "/" + date + 
              "/online_hosts/hosts_online_unsorted.txt | awk '{print $1}' | sed 's/.$//' | sort -u > " + output_path + "/" + date + "/online_hosts/" + date + "_online_hosts.txt")
    print(" [+] MassDNS done, creating altdns possibilites...")


def exec_massdns_final(output_path):
    RESOLVERS_PATH = "resolvers.txt"
    os.system('/root/massdns/bin/massdns -s 15000 -t A -o S -r ' + RESOLVERS_PATH + " --flush -w " + output_path + "/" + date + 
              "/online_hosts/" + date + "_altdns_online_unsorted_final.txt " + output_path + "/" + date + "/potential_subdomains/" + date + "_altdns_potential_subdomains.txt")

    os.system("cat " + output_path + "/" + date + "/potential_subdomains/" + date +
              "_altdns_potential_subdomains.txt | awk '{print $1}' | sort -u > " + output_path + "/" + date + "/online_hosts/" + date + "_altdns_online_hosts.txt")

    os.system("sort -u " + output_path + "/" + date + "/online_hosts/" + date + "_online_hosts.txt " + output_path + "/" + date +  
              "/online_hosts/" + date + "_altdns_online_unsorted_final.txt > " + output_path + "/" + date + "/online_hosts/final_online_hosts/final_online_hosts.txt")
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
        os.system('/snap/bin/amass enum -timeout 1 -df ' + str(domains_file) + ' | tee -a ' + file + '/' + date + '/potential_subdomains/' + date + '_amass_potential_subdomains.txt')

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
        #ffuf 80/443 for alive domains
        os.system('ffuf -c -w "' + file + "/" + date + '/online_hosts/final_online_hosts/final_online_hosts.txt:DOMAIN" -w /root/webports.txt -u http://DOMAIN/FUZZ -o ' + file + '/' + date + '/online_hosts/final_online_hosts/no_ssl_alive_fuzz.json -of json')
        with open(file + '/' + date + "/online_hosts/final_online_hosts/no_ssl_alive_fuzz.json") as ffuzjson:
            data = json.load(ffuzjson)

            for key in data['results']:
                if '403' in str(key['status']):
                    with open(file + "/" + date + '/online_hosts/final_online_hosts/403s/403_sites.txt', 'a') as g:
                        g.write(key['url'] + '\n')
                else:
                    with open(file + "/" + date + '/online_hosts/final_online_hosts/alive_sites/alive_sites.txt', 'a') as h:
                        h.write(key['url'] + '\n')


        #grep ips from final dns resolution
        ip_regex = r'([0-9]{1,3}[\.]){3}[0-9]{1,3}'
       # os.system('grep -E -o "'+ ip_regex + '" ' + file + '/' + date + '/online_hosts/final_online_hosts/final_online_hosts.txt > ' + file + '/' + date + '/online_hosts/final_online_hosts/for_ping_scan.txt')
        #ping scan 
        print(" [+] starting ping sweep for hosts resolved")
       # os.system('masscan -iL ' + file + '/' + date + '/online_hosts/final_online_hosts/for_ping_scan.txt -p 0 --ping -oG ' + file + '/' + date + '/online_hosts/final_online_hosts/responded_to_ping.txt')
        #grep ips from ping scan results
       # os.system('grep -E -o "'+ ip_regex + '" ' + file + '/' + date + '/online_hosts/final_online_hosts/responded_to_ping.txt > ' + file + '/' + date + '/online_hosts/final_online_hosts/for_port_scan.txt')
        #masscan all ports for ips from ping scan
       # os.system('masscan -iL ' + file + '/' + date + '/online_hosts/final_online_hosts/for_port_scan.txt -p 1-65535 --rate 15000 -oG ' + file + '/' + date + '/online_hosts/final_online_hosts/for_masscan_output_parser.txt')

        print('[+] parsing masscan file, building ultra dope final file :)')

        #remove masscan text from output
       # os.system("tail -n +3 " + file + "/" + date + "/online_hosts/final_online_hosts/for_masscan_output_parser.txt | head -n -1 > " + file + "/" + date + "/online_hosts/final_online_hosts/massscan_parse_work_file.txt")
       # os.system("touch " + file + "/" + date + "/online_hosts/final_online_hosts/all_servers_scanned.txt")
       # with open(file + "/" + date + "/online_hosts/final_online_hosts/massscan_parse_work_file.txt") as f:
        #for line of masscan output
       #     for line in f:
                #strip line of not needed text
       #         line2 = line.replace('Host: ', '').replace('()',' ').replace('Ports:','').replace('/open/tcp////','').strip()
                #grab ip, port from line in masscan output 
       #         print(line2)
       #         ip = line2[0:15].strip()
       #         port = line2.replace(ip, '').strip()
       #         ipandporttest = ip + port
       #         print("important: " + ipandporttest)
       #         with open(file + "/" + date + '/online_hosts/final_online_hosts/all_servers_scanned.txt', 'r+') as read_obj:
                    # Read all lines in the file one by one
       #             ipandport_home = str(ip + '     ' + port)
       #             not_in = True
       #             print("Testing: " + ip + ' ' + port)
       #             line_number = 0
       #             for line in read_obj:
       #                 line_number += 1
       #                 if ip in line:
       #                     if port not in line:
       #                         the_line = open(file + "/" + date + '/online_hosts/final_online_hosts/all_servers_scanned.txt').readlines()
       #                         print('         line with pair:' + str(line_number) + ' -> ' + the_line[line_number - 1])
       #                         the_line[line_number - 1] = line.strip() + ',' + port.strip() + '\n'
       #                         open(file + '/' + date + '/online_hosts/final_online_hosts/all_servers_scanned.txt','w+').write(''.join(the_line))

                            #print('!!! ip is at line -> ' +  str(returned)) 
       #                     not_in = False
       #                     break
                        #else:
                            #print('')
       #             if not_in == True:
       #                 read_obj.write(ipandport_home + '\n')
       #             else:
       #                 print('ip was in file')



                    # For each line, check if line contains the string


        #seperate hosts with port 80/443 into /web-servers/, /other-servers/
        print(" [+] enumeration complete for: " + file)