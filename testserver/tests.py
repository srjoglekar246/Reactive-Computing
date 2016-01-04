#Just some code to allow session-ed requests
from requests import Request, Session

s = Session()

def send_request(url, payload, file_to_write, reqtype="GET"):
    global s
    if reqtype == 'POST':
        req = Request(reqtype, url, data=payload)
    else:
        req = Request(reqtype, url, params=payload)
    prepped = s.prepare_request(req)
    resp = s.send(prepped, verify=False)
    f = open(file_to_write, 'w')
    f.write(resp.text)
    f.close()

serveraddr = "http://127.0.0.1:8000/"

#Input values
payload = {'input': '{"A": 4, "F": 5}'}
send_request(serveraddr+"input/", payload,
             '/home/srjoglekar/testout.html')
