import requests
import uuid
import sys
import os

# -- What to do if no input is given --
if len(sys.argv) == 1:
    print("Please provide an input such as: probe.py domains.txt",
          "For more help do probe.py -h")
    exit()

# -- The command the user issued, besides the python probe bit --
arguments = sys.argv[1:]


# -- Prints the help data --
def DisplayHelp():

    with open("help.txt", "r") as file:
        help = file.readlines()
        seperator = "\n"
        print(seperator.join(help))

    exit()


# -- Process input from a textfile --
def ProcessInput(file):

    folder = os.path.dirname(os.path.abspath(file))
    file = os.path.join(folder, file)

    with open(file, "r") as file:
        data = file.readlines()

    return [item.replace("\n", "") for item in data]


def ConstructRequest(host: str, protocol: str):
    return {
        "GET": "/ "+protocol+"/1.1",
        'Host': host,
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': "1",
        'Connection': 'close'
    }


# -- Store result in a text file --
def StoreResult(domain, port, content, code,
                fail=False, http=False, https=False):

    if not os.path.isdir(domain):
        os.mkdir(domain)
    os.chdir(domain)

    if http:
        if fail:
            print("Request on", "http://"+domain+":"+port, "failed")
        if not fail:
            print("http://"+domain+":"+port, code)

    if https:
        if fail:
            print("Request on", "https://"+domain+":"+port, "failed")
        if not fail:
            print("https://"+domain+":"+port, code)

    with open(str(uuid.uuid4())+".txt", "w") as file:

        if fail:
            file.write("Request failed")

        else:
            file.write("Server response on port" + port + " : " +
                       str(code) + "\n")
            file.write(str(content))
            file.close()

    os.chdir("..")


# -- Request Worker --
def TestForService(domain, port):

    # -- Try for http server --
    try:
        r = requests.get("http://"+domain+":"+str(port), 
                         headers=ConstructRequest(domain, "HTTP"))
        StoreResult(domain, port, r.text, r.status_code, http=True)

    # -- If one not found, record this --
    except:
        StoreResult(domain, port, "FAIL", "000", fail=True, http=True)

    # -- Try for https server --
    try:
        r = requests.get("https://"+domain+":"+str(port), 
                         headers=ConstructRequest(domain, "HTTPS"))
        StoreResult(domain, port, r.text, r.status_code, https=True)

    # -- If one not found, record this --
    except:
        StoreResult(domain, port, "FAIL", "000", fail=True, https=True)


# -- Initiator function --
def SendRequests(domainfile, ports):

    if not os.path.isdir("out"):
        os.mkdir("out")
    os.chdir("out")

    domains = ProcessInput(domainfile)
    for domain in domains:
        for port in ports:
            TestForService(domain, port)


# -- Checks if help mode is active --
if "-h" in arguments:
    DisplayHelp()

# -- Argument Parser --
for argument in arguments:

    # -- Process ports supplied by user --
    ports = ["80","443"]
    if "-p" in argument:
        argument.replace("-p", "")
        argument = argument.split(",")
        
        for port in argument:
            ports.append(str(port))

    # -- Process domains supplied by user --
    if ".txt" in argument:
        argument = os.path.realpath(argument)
        SendRequests(argument, ports)

