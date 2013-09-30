from twisted.internet import defer, reactor
from twisted.web.client import getPage
from bs4 import BeautifulSoup
hahaha = [1]

def pageCallback(result):
    return len(result)

def listCallback(result):
    return result

def finish(ign):
    reactor.stop()
    hahaha.append(ign)

def test():
    d1 = getPage('http://www.google.com')
    d1.addCallback(pageCallback)
    d2 = getPage('http://yahoo.com')
    d2.addCallback(pageCallback)
    dl = defer.gatherResults([d1, d2])
    dl.addCallback(listCallback)
    dl.addCallback(finish)

test()
print "begin"
reactor.run()
print "after"
print hahaha
