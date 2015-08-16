#!/usr/bin/python3

"""
Title: cgi_test.py
Language: python3
Author: Troy Caro <twc17@pitt.edu>
Purpose: Testing some SSH stuff
"""

import sys
import socket
import paramiko

# Here is where the magic starts
import cgi
import cgitb

# INPUT
def port_address(port):
    port_num = port.split("-")
    cmd  = "sh int status | incl " + port_num[2] 

    hst = port_num[1] + "-a-1.c3850.net.pitt.edu"

    if (check_host(hst) == 1):
        return hst, cmd
    else:
        hst = port_num[1] + "-a-1.c3750.net.pitt.edu"
        if (check_host(hst) == 1):
            return hst, cmd
        else:
            print("<p> Hmm, couldn't find the switch based on that port address :/ </p>")
            sys.exit(1)

# EXECUTE
def check_host(hst):
    """
    Trys to resolve the hostname

    Pre-conditions:
            Hostname is formatted correctly
    Post-conditions:
            Returns 1 if the hostname resolves, 0 if it does not
    """
    try:
        socket.gethostbyname(hst)
        return 1
    except socket.error:
        return 0

def execute(hst, usr, passwd, cmd):
    """
    Executes command on ssh server and returns output
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hst, 22, usr, passwd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read().strip()
    except paramiko.ssh_exception.AuthenticationException as e:
        print("<p> Oops, looks like you entered your username or password wrong :/ </p>")
        sys.exit(1)

    return output.decode(encoding='UTF-8')


# Start
print("Content-type:text/html\r\n\r\n")       

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get port address from html form
port = form.getvalue('port_address')
usr = form.getvalue('user_name')
passwd = form.getvalue('password')

print("""
<html>

<head><title>Port Lookup Tool</title></head>

<body>
""")
print("<h1>Results for <b>" + form.getvalue('port_address') + "</b></h1>" )

# Check to see if the port maps to a switch before going any further
# port_address() is set to exit if it can't find the switch
hst, cmd = port_address(port)
output = execute(hst, usr, passwd, cmd)

if (output == ""):
    print("<p> I found the switch, but not the port :/ </p>")
    # Haven't quite figured out the best way to handle this yet
    print("<p> If the device is connected, you can try searching by MAC address <a href='mac_search.html?port_address='" + port + "'>here</a>. </p>")
    sys.exit(1)

print("<p>" + output + "</p>")
print("""
</body>
</html>
""")
