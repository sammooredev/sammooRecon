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



control flow:           1. run amass, append to potential_subdomains.txt    
                        2. run commonspeak2, append to potential_subdomains.txt
                        3. run fdns-enum, append to potential_subdomains.txt
                        4. run massdns on potential_subdomains.txt, output alive_sub_domains.txt
                        5. run altdns on alive_sub_domains.txt output altdns_potential_subdomains.txt
                        6. run massdns on altdns_potential_subdomains, append to alive_sub_domains.txt 
                        7. 
                        8. enumeration finished.