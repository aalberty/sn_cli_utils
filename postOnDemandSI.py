import requests as r
import argparse, sys, json

#TODO: Config file support so you don't have to type your username and password every time

def throwError(msg):
    sys.exit("Error. " + msg + " Use -h for details.")

def validateInput(param):
    if param == None or param == "":
        return True
    
    if not type(param) == type(""):
        throwError ("Please provide string values for all parameters supplied.")
    
    return False


p = argparse.ArgumentParser(description="Insert a new on-demand script include to the specified ServiceNow instance.")
# name
p.add_argument("-n", "--name", help="Script Include suffix. For an on-demand script include, this **must** match the name of the function passed.")
# description
p.add_argument("-d", "--description", help="Script Include description. 'On Demand' appended to the end by default for filtering purposes.")
# script contents
p.add_argument("-b", "--body", help="Path to the file containing the Script Include script content.")
# host url
p.add_argument("--url", help="Hostname of the target instance in format 'https://<hostname>.service-now.com'")
# username
p.add_argument("-u", "--username", help="Username used for authentication to the API.")
# password
p.add_argument("-p", "--password", help="Password used for authentication to the API.")

args = p.parse_args()

# Input validation
if validateInput(args.url):
    throwError ("Please provide a host url to connect to." )

if args.url[-1] == "/":
    args.url = args.url[0:-1]

if validateInput(args.username) or validateInput(args.password):
    throwError ("Please provide valid authentication information. Username and/or password is missing.")

if validateInput(args.body):
    throwError ("Please provide the path to the file to fill the script body.")

if len(args.body) < 3 or not args.body[-3:] == ".js":
    throwError ("Please ensure the file referenced is a javascript file ending with file extension '.js'.")

if args.description == None:
    args.description = ""
# End input validation

args.description = args.description + "\nOn Demand script include"

url_suffix = "/api/now/table/sys_script_include"
headers = {"Content-Type":"application/json","Accept":"application/json"}
f = open(args.body)
data = {
    "name": args.name,
    "description": args.description,
    "access": "public",
    "script": f.read()
}

res = r.post(args.url + url_suffix, json=data, headers=headers, auth=(args.username, args.password), verify=False)
print (res)
