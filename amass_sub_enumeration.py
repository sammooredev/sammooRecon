import os

#spawn amass process

def amassSpawner():
    os.system('/snap/bin/amass enum -df domains.txt >> amass_potential_subdomains.txt')
    
amassSpawner()
    