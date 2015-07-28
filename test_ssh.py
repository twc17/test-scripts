#!/usr/bin/python3

"""
Title: test_ssh.py
Language: python
Author: Troy Caro <twc17@pitt.edu>
Purpose: Testing some SSH stuff
"""

import sys
import subprocess

# INPUT
def ui():
    """
    Gets console input for username to host

    Pre-conditions:
            The input is formatted correctly
            The username is entered correctly
            The host is alive, accepting connections
            Command is valid

    Post-conditions:
        Returns the username, host, and command
    """
    try:
        host = input("Enter the hostname or ip address: ")
        user = input("Enter the username for the remote host: ")
        cmd = input("Enter the command you would like to execute: ")
    except KeyboardInterrupt:
        print()
        print()
        print("Caught KeyboardInterrupt, terminating!")
        print()
        sys.exit(1)

    return user, host, cmd

# EXECUTE
def execute(h, u, c):
    """
    Executes command on ssh server and returns output
    """
    l = u + "@" + h
    return subprocess.check_output(['ssh','-o', 'StrictHostKeyChecking=no', '-o', 'ConnectTimeout=10', l, c], universal_newlines=True)

# MAIN
def main():
    """
    Main program function
    """
    u, h, c = ui()
    print(execute(h, u, c))

# RUN
if __name__ == "__main__":
    main()
