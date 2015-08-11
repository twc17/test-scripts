#!/usr/bin/python3

"""
Title: cgi_test.py
Language: python3
Author: Troy Caro <twc17@pitt.edu>
Purpose: Testing some SSH stuff
"""

import sys
import socket
import getpass
import paramiko

# Here is where the magic starts
import cgi
import cgitb

# INPUT
def ui():
    """
    Gets console input for username to host

    Pre-conditions:
            The input is formatted correctly
            The username is entered correctly

    Post-conditions:
        Returns the username
    """
    try:
        user = input("Enter your AD username: ")
        passwd = getpass.getpass("Enter the password for " + user + ": ")
    except KeyboardInterrupt:
        print()
        print()
        print("Caught KeyboardInterrupt, terminating!")
        print()
        sys.exit(1)

    return user, passwd

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
            print("""
            <p> Hmm, couldn't find the switch based on that port address :/ </p>
            </body>
            </html>
            """)
            sys.exit(1)

def search_mac():
    """
    Constructs command based on MAC address

    Pre-conditions:
            The MAC address is formatted correctly
            xxxx.xxxx.xxxx
    Post-conditions:
            Returns the command to run
    """
    try:
        mac = input("Enter the MAC address to search for on this switch: ")
    except KeyboardInterrupt:
        print()
        print("Caught KeyboardInterrupt, terminating!")
        print()
        sys.exit(1)

    return "sh mac add | incl " + mac

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
        print()
        print("Oops, looks like you entered your username or password wrong :/")
        print()
        sys.exit(1)

    return output.decode(encoding='UTF-8')


# Start
print("""
Content-type:text/html\r\n\r\n       
<html>

<head><title>Port Lookup Tool</title></head>
<h><b>Testing real-time port look-up tool</h>

<body>
""")

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get port address from html form
port = form.getvalue('port_address')

# Check to see if the port maps to a switch before going any further
# port_address() is set to exit if it can't find the switch
hst, cmd = port_address(port)
print(execute(hst, usr, passwd, cmd))
print("""
</body>
</html>
""")
