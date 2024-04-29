# -*- encoding: utf-8 -*-
'''
@File    :   decrypt.py
@Time    :   2024/04/29 11:44:25
@Author  :   castor sun 
@Contact :   suncheng@cmss.chinamobile.com
'''

import argparse

from cryptography.fernet import Fernet

def load_key():
    return open("key.key", "rb").read()

def decrypt_file(file_name, key):
    f = Fernet(key)
    with open(file_name, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(file_name, "wb") as file:
        file.write(decrypted_data)

def parse_args():
    parser = argparse.ArgumentParser(description="parameters")
    parser.add_argument('-i', '--input', nargs='*',help="src file")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    key = load_key()
    for ele in args.input:
        decrypt_file(ele, key)
    print ("done!")