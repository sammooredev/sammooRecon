import subprocess
from fileinput import filename


#create/open output file
outputFile = open("output.txt","a")

#spawn amass process
def amassSpawner(domain):

    amassprocess = subprocess.Popen(['amass', 'enum', '-d', str(domain)], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)
    while True:
        output = amassprocess.stdout.readline()
        outputFile.write(output)
        print(output.strip())
        return_code = amassprocess.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output 
            for output in amassprocess.stdout.readlines():
                print(output.strip())
            break

amassSpawner('google.com')