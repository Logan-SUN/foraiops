# -*- encoding: utf-8 -*-
'''
@File    :   encrypt.py
@Time    :   2024/04/29 11:41:42
@Author  :   castor sun 
@Contact :   suncheng@cmss.chinamobile.com
'''

import argparse

from cryptography.fernet import Fernet

def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    return key

def encrypt_file(file_name, key):
    f = Fernet(key)
    with open(file_name, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(file_name, "wb") as file:
        file.write(encrypted_data)

def parse_args():
    parser = argparse.ArgumentParser(description="parameters")
    parser.add_argument('-i', '--input', nargs='*',help="src file")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args=parse_args()
    key=write_key()
    for ele in args.input:
        encrypt_file(ele, key)    
    print ("done!")