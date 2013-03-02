#!/usr/bin/python
'''
NAME: client.py
DESC: Retrieve system information from the remote host.
      Create 'servercfg' file and list all the server that's running the
      inventry-agent.py program.
LAST REVISION: 18 Dec 2012
AUTHOR: Gene Ordanza <geronimo.ordanza@fisglobal.com>
'''

# Module declaration
from socket import *
from xmlrpclib import ServerProxy
from optparse import OptionParser
import sys

# Variable declaration
url  = 'http://%s:%s'
port = '9000'
file = 'servercfg'
desc = 'Retrieves system information from the remote hosts.'

# Function to retrieve the information from the server.
# Open the file, iterate over the IP addresses, connect to remote host and
# finally retrieve and display the information.
def getInfo():
    fp = open(file)
    try:
        for line in fp:
            host = url % (line.strip(), port)
            server = ServerProxy(host, allow_none=False)
            print '|'.join([str(string) for string in server.retrieveInfo()])
    finally:
        fp.close()

# Function to check if the inventory service is running on the remote host
# Open the file, iterate over the IP addresses, probe if port on the remote host
# is handling request. Display if service is ok or failed.
def checkServer():
    fp = open(file)
    try:
        for line in fp:
            sock = socket(AF_INET, SOCK_STREAM)
            if (sock.connect_ex((line, int(port))) == 0):
                print 'checking %s ... ok' % line.strip()
            else:
                print 'checking %s ... failed' % line.strip()
    finally:
        fp.close()

# Main function mostly for handling command line arguments.
# If '--check' option is used, check the inventory service on the remote host.
# If '--get' option is used, retrieve the inventory data from the remote host.
def main():
    parser = OptionParser(description=desc, usage="%prog [options]",
                          version="%prog 0.1")

    parser.add_option('-c', '--check', default=False, action="store_true",
                      help="Probe remote host if inventory service is running")

    parser.add_option('-g', '--get', default=False, action="store_true",
                      help="Retrieve system information from the remote host")

    option, args = parser.parse_args()

    if option.check:
        checkServer()

    if option.get:
        getInfo()

    if len(sys.argv) == 1:
        print "Run \"%s -h\" to display help message" % sys.argv[0]

if  __name__ == '__main__':
    main()
