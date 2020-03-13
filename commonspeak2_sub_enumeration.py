#This function generates potential subdomains by appending words to domain eg: foo.google.com
def CommonSpeakSubGen(domain):
    scope = str(domain)
    wordlist = open('./commonspeak2.txt').read().split('\n')
    outputFile = open("potential_subdomains/commonspeak2_potential_subdomains.txt","a")

    for word in wordlist:
        if not word.strip():
            continue
        outputFile.write('{}.{}\n'.format(word.strip(), scope))


with open("domains.txt", "r") as domain_list:
    #iterate through domains.txt
    for domain in domain_list:
        #fixed_domain is a line stripped of whitespace/newlines
        fixed_domain = domain.strip()
        #run commonspeak function for each line of domains.txt
        CommonSpeakSubGen(fixed_domain)