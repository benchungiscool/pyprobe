import requests
import uuid
import sys
import os

# -- what to do if no input is given --
if len(sys.argv) == 1:
    print("Please provide an input such as: probe.py domains.txt",
          "For more help do probe.py -h")
    exit()

# -- take data from the arguments --
arguments = sys.argv[1:]

# -- prints the help data --
def displayhelp():
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


# -- Store result in a text file --
def StoreResult(domain, content, code, httpfail=False, httpsfail=False):

    if not os.path.isdir(domain):
        os.mkdir(domain)
    os.chdir(domain)

    with open(str(uuid.uuid4())+".txt", "w") as file:

        if httpfail or httpsfail:
            file.write("Request failed")
               
        else:
            file.write("Server response: " + str(code) + "\n")
            file.write(request)
            file.close()

    os.chdir("..")


# -- Request Worker --
def TestForService(domain, port):
    
    # -- Try for http server --
    try:
        r = requests.get("http://"+domain)
        StoreResult(domain, r.content, r.status_code)
        print("http://"+domain, r.status_code)

    # -- If not, record this
    except:
        StoreResult(domain, "FAIL", "000", httpfail=True)

    # -- Try for https server --
    try:
        r = requests.get("https://"+domain)
        StoreResult(domain, r.content, r.status_code)
        print("https://"+domain, r.status_code)

    # -- If not, record this --
    except:
        StoreResult(domain, "FAIL", "000", httpfail=True)

    
# -- Initiator function --
def SendRequests(domainfile, ports):

    if not os.path.isdir("out"):
        os.mkdir("out")
    os.chdir("out")

    domains = ProcessInput(domainfile)
    for domain in domains:
        for port in ports:
            TestForService(domain, port)


# -- conditionals for the input from the command args --
# -- checks if help mode is active --
if "-h" in arguments:
    displayhelp()

# -- Argument Parser --
for argument in arguments:

    # -- if argument is ports --
    if "-p" in argument:
        print("Port support coming in a future update, check github")

    # -- if argument is a text file --
    if ".txt" in argument:
        argument = os.path.realpath(argument)
        SendRequests(argument, [80,443])

