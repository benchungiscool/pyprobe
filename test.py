import requests

def ConstructHeaders(domain):
    device = {
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': "1",
        'Connection': 'close'
    }
    return device


domain = "http://uber.com"

sesh = requests.Session()
req = requests.Request("GET", domain, headers=ConstructHeaders(domain))
prepped = req.prepare()

r = sesh.send(prepped)
print(r.status_code)
