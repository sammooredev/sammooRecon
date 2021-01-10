# sammooRecon
Recon Automation

droplet_enum_main.py & droplet_attack_main.py

  a mess of python I *used* to use for bug bounty recon. Would be very hard to run on anyones computer but my own :) lol.

OpenRedirector2 - again, good luck

  A script that:

  1. takes in a list of urls
  2. appends common open-redirect payloads to the url -> adds to testing list
  3. takes https://github.com/lc/gau output -> greps lines that inlcude "=http" -> replaces with them http://www.google.com -> adds to testing list
  4. requests all urls in the testing list, if any redirect to google.com it outputs to results.txt
