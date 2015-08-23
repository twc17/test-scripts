#!/usr/bin/python3

"""
Title: helper.py
Language: python3
Author: Troy Caro <twc17@pitt.edu>
Project Purpose: To provide the Helpdesk with a more accurate tool for getting information about end-user devices
File Purpose: Helper functions for port_serch.py and mac_search.py
"""

# Import statements
import sys
import socket
import paramiko
import cgi
import cgitb

"""
Description:
    Based on the port description, this function will attempt to locate the correct switch,
    and assemble a command to show the status of the interface associated with the 
    port description

    The function will try to determine the switch based off of the center portion of the
    port description. Sticking with the PittNET naming convention, it will first try
    to connect to a c3850, then a c3750. If both of those lookups fail, the program will exit

Variables:
    port - The port description

Returns:
    hst - The hostname of the switch
    cmd - The command to run on the switch
"""
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

"""
Description:
    Check to see if a given hostname resolves to an IP address.

Variables:
    hst - The hostname to check

Returns:
    Will return 1 if the hostname resolves, 0 if it does not
"""
def check_host(hst):
    try:
        socket.gethostbyname(hst)
        return 1
    except socket.error:
        return 0

"""
Description:
    Runs a command against a host over SSH protocol on default port 22

Variables:
    hst - The host to connect to
    usr - The username used to authenticate
    passwd - Password for 'usr'
    cmd - The command to run on the host machine

Returns:
    Output of command run on remote host
"""
def execute(hst, usr, passwd, cmd):
    ssh = paramiko.SSHClient()
    # Set AutoAddPolicy so that we are not prompted to add new hosts to know_hosts file
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # All PittNET switches run SSH on default port 22
        ssh.connect(hst, 22, usr, passwd)
        # stdin, stdout, sterr are all set here, could write if needed
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read().strip()
    except paramiko.ssh_exception.AuthenticationException as e:
        print("<p> Oops, looks like you entered your username or password wrong :/ </p>")
        sys.exit(1)

    # stdout is written in 'bytes'. Needs to be decoded before priting
    return output.decode(encoding='UTF-8')
