#!/usr/bin/python3

"""
Title: test_ssh.py
Language: python3
Author: Troy Caro <twc17@pitt.edu>
Purpose: Testing some SSH stuff
"""

import sys
import socket
import subprocess

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
    except KeyboardInterrupt:
        print()
        print()
        print("Caught KeyboardInterrupt, terminating!")
        print()
        sys.exit(1)

    return user

def port_address():
    """
    Gets user input for the port addres.

    Pre-conditions:
            The port address is formatted correctly
    Post-condititons:
            Returns the switch (host) to connect to, and the command to run
    """
    try:
        port = input("Enter the port address: ")
    except KeyboardInterrupt:
        print()
        print()
        print("Caught KeyboardInterrupt, terminating!")
        print()
        sys.exit(1)

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
            print()
            print("Hmmm, couldn't find the switch based on that port, pass to the NOC")
            print()
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

def execute(hst, usr, cmd):
    """
    Executes command on ssh server and returns output
    """
    login = usr + "@" + hst
    try:
        output = subprocess.check_output(['ssh','-o', 'StrictHostKeyChecking=no', '-o', 'ConnectTimeout=10', login, cmd], universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print()
        raise

    return output

# MAIN
def main():
    """
    Main program function
    """
    usr = ui()
    hst, cmd = port_address()
    output = execute(hst, usr, cmd)

    if (output == ""):
        print()
        search = input("Hmm, couldn't find that port address, would you like to search by MAC address on this switch? (Y/N) ")

        if (search == 'Y'):
            output = execute(hst, usr, search_mac()) 
        else:
            sys.exit(1)

    print(output)

# RUN
if __name__ == "__main__":
    main()
