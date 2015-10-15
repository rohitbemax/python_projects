from twisted.internet import reactor, defer
from connectiontester import testConnect

def handleAllResults(results, ports):

    for port, resultInfo in zip(ports, results):
        success, result = resultInfo
        if success:
            print "Connected to port %i" % port

    reactor.stop()



import sys
host = "199.63.244.171"
ports = [10000, 10000, 10000]
testers = [testConnect(host, port) for port in ports]
defer.DeferredList(testers, consumeErrors=True).addCallback(handleAllResults, ports)
reactor.run( )