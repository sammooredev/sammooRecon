#code by 0xpatrik :)

import json
import subprocess

RESOLVERS_PATH = 'resolvers.txt'

def _exec_and_readlines(cmd, domains):

    domains_str = bytes('\n'.join(domains), 'ascii')
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.PIPE)
    stdout, stderr = proc.communicate(input=domains_str)

    return [j.decode('utf-8').strip() for j in stdout.splitlines() if j != b'\n']

def get_massdns(domains):
    massdns_cmd = [
        '/home/sam/massdns/bin/massdns',
        '-s', '15000',
        '-t', 'A',
        '-o', 'J',
        '-r', RESOLVERS_PATH,
        '--flush'
    ]

    processed = []

    for line in _exec_and_readlines(massdns_cmd, domains):
        if not line:
            continue

        processed.append(json.loads(line.strip()))

    return processed

print(get_massdns(['google.com', 'sub.google.com']))