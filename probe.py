import requests
import sys
import os

## What to do if no input is given
if len(sys.argv) == 1:
    print("Please provide an input such as: probe.py domains.txt",
          "For more help do probe.py -h")
    exit()

## Take input from the run command 
arguments = sys.argv[1:]


## Prints the help data 
def DisplayHelp():

    with open("help.txt", "r") as file:
        help = file.readlines()
        seperator = "\n"
        print(seperator.join(help))

    exit()


## Process input from a textfile 
def ProcessInput(file):

    ## Find the file specified
    folder = os.path.dirname(os.path.abspath(file))
    file = os.path.join(folder, file)

    ## Read from file
    with open(file, "r") as file:
        data = file.readlines()

    ## Removes all linebreaks from returned data
    data = [item.replace("\n", "") for item in data]

    ## Removes blank items in data
    for item in data:
        if not item:
            data.remove(item)

    return data


## Returns headers for the request
def ConstructHeaders():
    return {
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

    # -- Create folder where result will go --
    if not os.path.isdir(domain):
        os.mkdir(domain)
    os.chdir(domain)

    # -- Print response status if in verbose mode --
    if verbose and not fail:
        if http:
            print("http://"+domain+":"+port, code)

        if https:
            print("https://"+domain+":"+port, code)

    # -- Write repsonse to file --
    with open(domain+str(code)+".html", "w") as file:
        file.write(str(content))
        file.close()

    # -- Move up for next result --
    os.chdir("..")


# -- Request Worker --
def TestForService(domain, port, session):

    ## Make some headers for a request 
    headers = ConstructHeaders()

    ## Construct http request 
    req = requests.Request("GET", "http://"+domain+":"+str(port),
                           headers=headers)
    prepped = req.prepare()

    ## Send request
    try:
        r = session.send(prepped)
        StoreResult(domain, port, r.text, r.status_code, http=True)

    ## If request doesn't work, move on 
    except:
        pass

    ## Construct https request
    req = requests.Request("GET", "https://"+domain+":"+str(port),
                           headers=headers)
    prepped = req.prepare()

    ## Send request
    try:
        session.send(prepped)
        StoreResult(domain, port, r.text, r.status_code, https=True)

    ## If it doesn't work, move on
    except:
        pass


## Inititate scan
def SendRequests(domainfile, ports):

    if not os.path.isdir("out"):
        os.mkdir("out")
    os.chdir("out")

    session = requests.Session()

    domains = ProcessInput(domainfile)
    for domain in domains:
        for port in ports:
            TestForService(domain, port, session)


## Checks if the user has called help mode
if "-h" in arguments:
    DisplayHelp()

## Argument Parser
for argument in arguments:

    ## Process ports supplied by user
    ports = ["80","443"]
    if "-p" in argument:
        argument.replace("-p", "")
        argument = argument.split(",")
        
        for port in argument:
            ports.append(str(port))
    
    ## Check for verbose mode, turn off by default
    verbose = False
    if "-v" in argument:
        verbose = True

    ## Process domains supplied by user
    if ".txt" in argument:
        argument = os.path.realpath(argument)
        SendRequests(argument, ports)

