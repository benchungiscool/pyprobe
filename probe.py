import sys
import os
import socket
import uuid

# -- what to do if no input is given --
if len(sys.argv) == 1:
    print("Please provide an input such as: probe.py domains.txt",
          "For more help do probe.py -h")
    exit()

# -- take data from the arguments --
arguments = sys.argv[1:]

# -- prints the help data --
def displayhelp():
    print("""
    PyProbe by Ben Chung

    Usage: 
    python3 probe.py [arguments] [-h] 

    Filename = a arguments, preferably a text file, from which to
    read the domains to check on.
    -h = Print help info then exit
    """)
    exit()


# -- process input from a textfile --
def ProcessInput(file):
    print("P", file)
    with open(file, "r") as file:
        data = data.readlines()
    return [item.replace("\n", "") for item in data]


# -- Store result in a text file --
def StoreResult(domain, request, code):
    if not os.path.isdir(domain):
        os.mkdir(domain)
    os.chdir(domain)
    
    with open(uuid.uuid4(), "w") as file:
        file.write("Server response: " + code + "\n")
        file.write(request)
        file.close()


# -- request worker --
def TestForService(domain, port):

    if port == 443:
        connection = http.client.HTTPSConnection(domain, port)
        connection.request("GET", "/")
        response = connection.getresponse()
        print("HTTP Server on " + domain + str(response))
        StoreResult(domain, response.read(), response)

    if port == 80:
        connection = http.client.HTTPConnection(domain, port)
        connection.request("GET", "/")
        response = connection.getresponse()
        print("HTTP Server on " + domain + str(response))
        StoreResult(domain, response.read(), response)


# -- Initiator function --
def SendRequests(domainfile, ports):
    domains = processinput(domainfile)
    for domain in domains:
        for port in ports:
            TestForService(domain, port)


# -- conditionals for the input from the command args --
# -- checks if help mode is active --
if "-h" in arguments:
    displayhelp()

# -- Makes output dir, then cds in --
if not os.path.isdir("out"):
    os.mkdir("out")
os.chdir("out")

# -- Argument Parser --
for argument in arguments:

    # -- if argument is ports --
    if "-p" in argument:
        print("Port support coming in a future update, check github")

    # -- if argument is a text file --
    if ".txt" in argument:
        SendRequests(argument, [80,443])

