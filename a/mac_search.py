#!/usr/bin/python3

"""
Title: mac_search.py
Language: python3
Author: Troy Caro <twc17@pitt.edu>
Purpose: Search Cisco Catalyst series switches on PittNET by MAC address
"""

from helper import *

# Start
print("Content-type:text/html\r\n\r\n")       

# Create instance of FieldStorage
form = cgi.FieldStorage()

port = form.getvalue('port_address')
usr = form.getvalue('user_name')
passwd = form.getvalue('password')
mac = form.getvalue('mac_address')

print("""
<html>

<head><title>Port Lookup Tool</title></head>

<body>
""")
print("<h1>Results for <b>" + mac + "</b></h1>" )

# Check to see if the port maps to a switch before going any further
# port_address() is set to exit if it can't find the switch
hst, cmd = port_address(port)
output = execute(hst, usr, passwd, ("sh mac add | incl " + mac))

if (output == ""):
    print("<p> Doesn't look like that device is connected </p>")
    print("<p> If the device is really connected, it could be indicating some kind of issue </p>")
    sys.exit(1)

output = execute(hst, usr, passwd, ("sh int status | incl " + output.split()[3]))

print("<p>" + output + "</p>")
print("""
</body>
</html>
""")
