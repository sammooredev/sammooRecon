import glob
import time
import json
import os
from os import path
import datetime
from OpenRedirector2 import main, textFormatter, fileSplit

grabdate = datetime.datetime.now().date()
date = str(grabdate)

program_path = "/root/Bounty/*"

for file in glob.glob(program_path):
    dir_path = str(file) + "/*"
    for file in glob.glob(dir_path):
        if "__pycache" in file:
            pass
        else:
            print("Starting Post-Enumeration for: " + file)


            # make dir for dirfuzz
            os.system('mkdir ' + file + '/' + date +
                       '/online_hosts/final_online_hosts/alive_sites/dirfuzz')

             # dir fuzz
             #use ffuf to do all domains and wordlist at once
            #os.system('ffuf -c -w "' + file + "/" + date + '/online_hosts/final_online_hosts/alive_sites/alive_sites.txt:DOMAIN" -w /usr/share/wordlists/big.txt -u DOMAIN/FUZZ -t 200 -o ' +
            #           file + "/" + date + '/online_hosts/final_online_hosts/alive_sites/dirfuzz/dirfuzz.json -of json')

            #ffuf one domain at a time, auto calibrate filtering

            #with open(file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/dirfuzz/dirfuzz.json') as dirfuzzjson:
            #     data = json.load(dirfuzzjson)

            #     for key in data['results']:
            #         if '200' in str(key['status']):
            #             with open(file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/dirfuzz/200s.txt', 'a') as g:
            #                 g.write("200 - " + key['url'] + '\n')
            #         else:
            #             with open(file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/dirfuzz/other.txt', 'a') as h:
            #                 h.write(str(key['status']) + " - " + key['url'] + '\n')

            # subjack
            # make dir for subjack
            os.system('mkdir ' + file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/subjack')

            # # run subjack
            print('running subjack...')
            os.system('subjack -w ' + file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/alive_sites.txt -t 150 -timeout 5 -o ' + file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/subjack/results.txt')
            # gau 
            os.system('mkdir ' + file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/gau')
            os.system('cat ' + file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/alive_sites.txt | cut -d / -f 3-4 | cut -d / -f 1-1 | gau | tee -a ' + file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/gau/for_grep.txt')
            os.system('cat ' + file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/gau/for_grep.txt | grep =http | tee -a ' + file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/gau/for_anti_burl.txt')
            # anti-burl
            os.system('cat ' + file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/gau/for_anti_burl.txt | anti-burl | tee -a ' + file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/gau/fix-up.txt')
            os.system('cat ' + file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/gau/fix-up.txt | cut -c 21- | tee -a ' + file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/gau/gau_results_final.txt')
            
            #open-redirector
            if path.exists(file + "/" + date + "/online_hosts/final_online_hosts/alive_sites/gau/gau_results_final.txt") == True:
                os.system('mkdir ' + file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/OpenRedirector2')
                main(file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/alive_sites.txt', file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/gau/gau_results_final.txt', file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/OpenRedirector2/')
            
            # run masscan on found ips, sort and shit
            ip_regex = r'([0-9]{1,3}[\.]){3}[0-9]{1,3}'
            # ping sweep
            os.system('masscan -iL ' + file + '/' + date + '/online_hosts/for_ping_scan.txt -p 0 --ping -oG ' + file + '/' + date + '/online_hosts/responded_to_ping.txt')
             # grep ips from ping sweep results
            os.system('grep -E -o "' + ip_regex + '" ' + file + '/' + date + '/online_hosts/responded_to_ping.txt > ' + file + '/' + date + '/online_hosts/for_port_scan.txt')
            # masscan all ports for ips from ping scan
            os.system('masscan -iL ' + file + '/' + date + '/online_hosts/for_port_scan.txt -p 1-65535 --rate 15000 -oG ' + file + '/' + date + '/online_hosts/for_masscan_output_parser.txt')

            print('[+] parsing masscan file, building ultra dope final file :)')

            os.system("tail -n +3 " + file + "/" + date + "/online_hosts/for_masscan_output_parser.txt | head -n -1 > " + file + "/" + date + "/online_hosts/for_masscan_parse.txt")
            os.system("mkdir " + file + "/" + date + "/online_hosts/final_online_hosts/alive_sites/masscan")
            os.system("touch " + file + "/" + date + "/online_hosts/final_online_hosts/alive_sites/masscan/all_servers_scanned.txt")

            with open(file + "/" + date + "/online_hosts/for_masscan_parse.txt") as f:
                 # for line of masscan output
                 for line in f:
                     # strip line of not needed text
                     line2 = line.strip().replace('Host: ', '').replace(
                         '()', '       ').replace('Ports: ', '').replace('/open/tcp////', '')
                     # grab ip, port from line in masscan output
                     print(line2)
               
                     ip = line2[0:15].strip()
                     port = line2.replace(ip, '').strip()
                   
                     with open(file + "/" + date + '/online_hosts/final_online_hosts/alive_sites/masscan/all_servers_scanned.txt', 'r+') as read_obj:
                         # Read all lines in the file one by one
                         ipandport_home = str(ip + ' ' + port)
                         not_in = True
                         print("Testing: " + ip + ' ' + port)
                         line_number = 0
                         for line in read_obj:
                             line_number += 1
                             print(line_number)
                             if ip in line:
                                 if port not in line:
                                     the_line = open(
                                         file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/masscan/all_servers_scanned.txt').readlines()
                                     print('         line with pair -> ' +
                                           the_line[line_number - 1])
                                     the_line[line_number - 1] = line.strip() + ',' + port + '\n'
                                     open(file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/masscan/all_servers_scanned.txt', 'w+').write(''.join(the_line))

                                 not_in = False
                         if not_in == True:
                             read_obj.write(ipandport_home + '\n')
                         else:
                             print('ip was in file')
            #SCREENSHOTs
            #httprobe found ips
            os.system('cat ' + file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/masscan/all_servers_scanned.txt | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" | httprobe | tee ' + file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/masscan/probed_ip_list.txt')
            #merge ip list and alive sites
            os.system('sort -u ' + file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/masscan/probed_ip_list.txt ' + file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/alive_sites.txt > ' + file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/ips_alive_sites_combined.txt')
            #screenshot
            #eyewitness
            #os.system('./../EyeWitness/Python/EyeWitness.py -f ' + file + "/" + date + "/online_hosts/final_online_hosts/alive_sites/ips_alive_sites_combined.txt --web --timeout 5 --max-retries 0  --threads 75 -d " + file + "/" + date + '/online_hosts/final_online_hosts/alive_sites/screenshots --results 500 --no-prompt')
            #webscreenshot
            os.system('xvfb-run webscreenshot -v -i ' + file + '/' + date + '/online_hosts/final_online_hosts/alive_sites/ips_alive_sites_combined.txt -w 50 -t 10 -o ' + file + '/' + date +  '/online_hosts/final_online_hosts/alive_sites/screenshots')
