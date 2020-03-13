import os

#spawn amass process

def amassSpawner():
    os.system('/snap/bin/amass enum -timeout 60 -df domains.txt >> potential_subdomains/amass_potential_subdomains.txt')
    
amassSpawner()
    