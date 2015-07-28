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
    except:
        print()
        print("Hmmm, something else happened. Send this to the dev team!")
        print()
        raise
        sys.exit(1)

    return user, host, cmd

# EXECUTE
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
    u, h, c = ui()
    print()
    print(execute(h, u, c))
    print()

# RUN
if __name__ == "__main__":
    main()
