Sam Moore - 5th Mar 2020
ProjectREADME: 

1. The goal of this project is to create a "set and forgot" system that:
    a. takes a list of (bug-bounty) domains -> 
    b. enumerates subdomains -> 
    c. runs tools on subdomains ->
    d. maintained in a sqlite database. 

Things to figure out:
    b. Python for subdomain enumeration:
            -script needs to run amass, pull rapid7DNSdataset + create possible subs from commonspeak2 wordlist + run massdns -> altdns for permuatations -> massdns
            -> output final list "subdomains.txt"
            
    c. Python for post-enum scanning:
            Tools to use:  
                -masscan port scanning
                -sub-brute/other subdomain hijack scanning tool? tko-subs? 
                -service fingerprinting for web ports/found ports -> wappalyzer?
                -gau for endpoint enumeration

    d. Creating a database:
        -what database? how to write it in python? gui?


Goals of this: 
    -learn to write in python - learn to create/manage a database, establish 0 need to spent time doing manual recon. Use git and update as I code.

    -Re-Run tools twice a week
        -Output found changes to text file? table? How to distinguish changes?

    -Uses of this database:
        -have massive dataset from which you can be the first to exploit CVEs. 
        -See company specific architecture patterns



control flow:          

 #This is the main file, wrapping the modules. Control flow for this program is: 
#1. run amass, append to amass_potential_subdomains.txt    
#       - run commonspeak2, append to commonspeak2_potential_subdomains.txt
#TO-DO: - run fdns-enum, append to fdns_potential_subdomains.txt
#3. merge amass_potential_subdomains, commonspeak2_potential_subdomains, and fdns_potential_subdomains to one file, all_potential_subdomains.txt
#2. run massdns on all_potential_subdomains.txt, output hosts_online_unsorted.txt, sort them, output hosts_online.txt, delete hosts_online_unsorted.txt
#3. run altdns on hosts_online.txt output altdns_potential_subdomains.txt
#4. run massdns on altdns_potential_subdomains, output to altdnsfound_online_unsorted.txt, sort, append to hosts_online.txt 
#5. enumeration finished.