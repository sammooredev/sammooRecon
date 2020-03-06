import os

#spawn amass process

def amassSpawner():
    os.system('amass enum -df domains.txt >> output.txt')

amassSpawner()

    
  
    