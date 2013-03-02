#!/usr/bin/python
'''
NAME: inventry-agent.py
DESC: Run an XMLRPC agent on the host server. The XMLRPC service would gather
      all host information on the server and relay them over port 9000 upon
      request from a client.
LAST REVISION: 18 Dec 2012
AUTHOR: Gene Ordanza <geronimo.ordanza@fisglobal.com>
'''

# Module declaration
from SimpleXMLRPCServer import SimpleXMLRPCServer
from commands import getoutput, getstatusoutput
from datetime import datetime
import platform
import socket
import sys

# Variable declaration for various component of the server
eth0 = "/sbin/ifconfig eth0"
eth1 = "/sbin/ifconfig eth1"
bond0 = "/sbin/ifconfig bond0"
cpuinfo = "cat /proc/cpuinfo"
memory  = (getoutput('free')).split('\n')[1].split(':')[1].split()[0]

# Get the first IP address on the server. First check whether network bonding is
# setup.  If not, get the IP on eth0 card.
def getIP1():
    if getstatusoutput(bond0)[0] == 0:
        return getoutput(bond0).split('\n')[1].split(':')[1].split()[0]
    elif getstatusoutput(eth0)[0] == 0:
        return getoutput(eth0).split('\n')[1].split(':')[1].split()[0]
    return None

# Create an instance of the XML-RPC server. Listen on port 9000 and log request
# on the console if server is running in the foreground.
server = SimpleXMLRPCServer((getIP1(), 9000), logRequests=True)

# Encapsulate the code for retrieving information into a class. Make most of the
# methods private to the class (except for retrieveInfo method which is declare
# public)
class ServerInfo(object):
    def __init__(self):
        print getIP1()
        self.hostinfo = [self._getHostName(), self._getDataCTR(),
                         self._getIP1(), self._getIP2(), self._getOSver(),
                         self._getKernelVer(), self._getDistroName(),
                         self._getDistroVer(), self._getCPUcount(),
                         self._getRAMsize(), self._getDate()]

    def _getHostName(self):
        return socket.gethostname()

    def _getDataCTR(self):
        return (socket.gethostname())[1:4].upper()

    def _getIP1(self):
        return getIP1()

    def _getIP2(self):
        if getstatusoutput(eth1)[0] == 0:
            return getoutput(eth1).split('\n')[1].split(':')[1].split()[0]
        return None

    def _getOSver(self):
        return platform.system()

    def _getKernelVer(self):
        return (platform.release()).split('-')[0]

    def _getDistroName(self):
        return (platform.dist()[0]).capitalize()

    def _getDistroVer(self):
        return platform.dist()[1]

    def _getCPUcount(self):
        return getoutput(cpuinfo).count('processor')

    def _getRAMsize(self):
        return memory

    def _getDate(self):
        return str(datetime.now()).split()[0]

    def retrieveInfo(self):
        return self.hostinfo

# Run the XML-RPC server instance to respond to requests from the clients.
server.register_instance(ServerInfo())

if  __name__ == '__main__':
    try:
        print 'Use Control-C to exit'
        # Wait on the port 9000 for any incoming request.
        server.serve_forever()
    except Exception, err:
        sys.stderr.write('ERROR: %s\n' % str(err))
        sys.exit(1)
