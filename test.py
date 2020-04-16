import requests

def ConstructHeaders(domain):
    device = {
        "GET": "/ HTTP/1.1",
        "Host": domain,
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': "1",
        'Connection': 'close'
    }
    return device

with open("domains.txt", "r") as file:

    domains = file.readlines()
    domains = [domain.replace("\n", "") for domain in domains]
    print(domains)

    for domain in domains:
        r = requests.get("http://"+domain, headers=ConstructHeaders(domain))
        print(r.status_code)
