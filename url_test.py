#!/usr/bin/env python
import re
import urlparse
import urllib2
from sgmllib import SGMLParser
import base64

def autotest_urlopen(url):
    req = urllib2.Request(url)
    base64string = \
        base64.encodestring('%s:%s' %
                            ('guzheng', 'guzheng4DdN')).replace('\n', '')
    req.add_header("Authorization", "Basic %s" % base64string)
    response = urllib2.urlopen(req)
    return response

res = autotest_urlopen('http://gerrit.datadirectnet.jp:8082/#/c/396/')
print str(res.read())
