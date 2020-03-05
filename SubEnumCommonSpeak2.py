

#This function generates potential subdomains by appending words to domain eg: foo.google.com
def CommonSpeakSubGen(domain):
    scope = str(domain)
    wordlist = open('./commonspeak2.txt').read().split('\n')
    outputFile = open("output.txt","a")

    for word in wordlist:
        if not word.strip():
            continue
        outputFile.write('{}.{}\n'.format(word.strip(), scope))