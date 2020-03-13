import requests,sys,time,os,argparse
import urllib.parse
from furl import furl
import re

#1.open list online_hosts
#2.grep & replace content starting with =http and ending at \n or &
#3.request vector, print final destination: domain + url response code (303) else print request not redirected


parser = argparse.ArgumentParser()

parser.add_argument('-d', help='path to file of domain list', nargs=1, dest='domain', required=True)

args = parser.parse_args()
    file with subdomains
file = args.domain[0]

with open(file) as domains:
	for line in domains:
		fixed_line = line.strip()
		print(fixed_line + " -- fetching waybackurls endpoints")
		os.system("/home/sam/go/bin/gau/gau.go " + fixed_line + " >> mass_wbu_endpoints_list.txt")

	print("\n\n\nDone with GAU, sorting, then redirect testing.\n\n\n")

	time.sleep(5)

	os.system('cat mass_wbu_endpoints_list.txt | grep "=http" >> endpoints_for_redirect_testing.txt')
	
	print("\n Done fetching endpoints...")

	print("\n Gonna start redirect testing...")

	time.sleep(5)

with open('endpoints_for_redirect_testing_sorted.txt') as waybackendpoints:
	for line in waybackendpoints:

		url_morphed = re.sub('=http.*?&','=https://www.google.com',str(line), flags=re.DOTALL)
		final_url = re.sub('=http.*?\n','=https://www.google.com',str(url_morphed), flags=re.DOTALL)
		print(final_url)
		response = requests.get(final_url, verify=True)
	
		if response.history:
			print("request redirected...")
			print(str(response.status_code) + ' ' + str(response.url))
			
			if "www.google.com" in response.url and str(response.status_code) != "404":

				foo = open("Possible_Open_Redirects.txt","a")
				foo.write('\n\n' + str(final_url) + "\n\nRedirected to:\n|\nV\n\n" + str(response.status_code) + " " + str(response.url) + "\n\n\n")
				
			for resp in response.history:

				print("|")
				print(resp.status_code, resp.url)

				print("final destination: " + str(resp.status_code) + str(resp.url)) 

		else:
			print("0")


	