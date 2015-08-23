#!/usr/bin/python3

"""
Title: port_search.py
Language: python3
Author: Troy Caro <twc17@pitt.edu>
Project Purpose: To provide the Helpdesk with a more accurate tool for getting information about end-user devices
File Purpose: Search Cisco Catalyst series switches on PittNET by port description
"""

# Import everything from helper, we'll need it!
from helper import *

# Start output to html page
print("Content-type:text/html\r\n\r\n")       

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get port address from html form
port = form.getvalue('port_address')
usr = form.getvalue('user_name')
passwd = form.getvalue('password')

# Setup CSS and page title
print("""
<html>

<head>

<link rel="stylesheet" type="text/css" href="../../style.css">

<title>Port Lookup Tool</title>

</head>
<body>
""")
print("<div class=\"center\">")
print("<h1>Results for <b>" + port + "</b></h1>" )

# Check to see if the port maps to a switch before going any further
# port_address() is set to exit if it can't find the switch
hst, cmd = port_address(port)

# If the output of execute is empty, then we know that we have the correct switch, but the port description isn't there.
# We'll ask the user if they want to search this switch by MAC address
output = execute(hst, usr, passwd, cmd)
if (output == ""):
    print("<p> I found the switch, but not the port :/ </p>")
    print("<p> If the device is connected, you can try searching by MAC address <a href='http://136.142.3.230/mac_search.html?port_address=" + port + "'>here</a>. </p>")
    sys.exit(1)

# Split output and get interface status (connected, notconnected, disabled, etc)
output = output.split()
mac_status = output[2]

# If the interface is showing connected, we'll want to also display the connected MAC address
if (mac_status == "connected"):
    mac_test = execute(hst, usr, passwd, ("sh mac add | incl " + output[0]))
    # This is a weird case where the interface is showing as connected, but the MAC address isn't showing up
    if (mac_test == ""):
        mac_status = "Hmm..? :/"
    else:
        mac_status = mac_test.split()[1]
else:
    mac_status = "None"

# Output results to html page
print("<p><b>Port Address: </b>" + output[1] + "</p>")
print("<p><b>Status: </b>" + output[2] + "</p>")
print("<p><b>VLAN: </b>" + output[3] + "</p>")
print("<p><b>Speed: </b>" + output[5] + "</p>")
print("<p><b>Duplex: </b>" + output[4] + "</p>")
print("<p><b>MAC: </b>" + mac_status + "</p>")
print("""
</div>
</body>
</html>
""")
