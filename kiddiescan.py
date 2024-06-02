#!/usr/bin/env python3
import nmap, os, sys, subprocess
from enum import Enum

# Global enumaration of all the scan types
class Enum(tuple): __getattr__ = tuple.index
ScanType = Enum(['STANDARD', 'QUIET', 'PANIC', 'LOUD', 'CTF'])

# And all the options
# TODO add the options for other scans
scanOptions = {
    "STANDARD": "-sV -T3 ",
    "QUIET": "-T2 -O -sS -sV -f -g 53 --data-length 10",
    "PANIC": "-T1 -O -sS -sV -f -g 53 --data-length 10 --",
    "LOUD": "-sV -T3 ",
    "CTF": "-sV -T3 "
}

def runScan(options, scanType):
    
    print(f"You've chosen {scanType.capitalize()}\nOptions that will be run: {options}")
    
    customOptions = input("Do you want to add custom options? y/n (n): > ")
    if customOptions.capitalize() == 'Y':
        customOptions = input("add all the additional options (ex. -p1-1000 ): > ")
        options+=customOptions
    
    # Script looks for default gateway from ip route and then formats it nicely
    gateway = subprocess.check_output("ip route | grep default | cut -d ' ' -f 3", shell=True).decode("UTF-8").rstrip('\n')
    # print(gateway)    
# I got a thing for retro ascii art
def printDetails():

    banner = '''
 _   __ _      _      _  _         _____                    
| | / /(_)    | |    | |(_)       /  ___|                    
| |/ /  _   __| |  __| | _   ___  \ `--.   ___   __ _  _ __  
|    \ | | / _` | / _` || | / _ \  `--. \ / __| / _` || '_ \ 
| |\  \| || (_| || (_| || ||  __/ /\__/ /| (__ | (_| || | | |
\_| \_/|_| \__,_| \__,_||_| \___| \____/  \___| \__,_||_| |_|
    '''
    print(banner)

# It's easier to run as root ngl
def getSU():
    euid = os.geteuid()
    if euid != 0:
        print("Script not started as root. Running sudo..")
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        os.execlpe('sudo', *args)

# Prints a nice menu with all the choices for scanning
def printMenu():
    print('Scan Types: ')
    for scan in [ScanType[k] for k in range(len(ScanType))]:
        print(f'{getattr(ScanType, scan)+1}. {scan.capitalize()}')
    try:
        choice = int(input("(1)> "))
    except ValueError:
        choice = 1
    if choice not in range(1,5):
        choice = 1
    choice -= 1
    
    runScan(scanOptions[ScanType[choice]], ScanType[choice])
    
def main():

    printDetails()
    printMenu()
main()