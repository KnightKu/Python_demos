#!/usr/bin/env python
import re
import urlparse
import urllib2
from sgmllib import SGMLParser
import base64


class URLLister(SGMLParser):

    def __init__(self, pattern):
        SGMLParser.__init__(self)
        self.urls = []
        self.is_done = False
        self.target_ref = ""
        self.pattern = pattern
        self.dirs = {}

    def start_a(self, attrs):
        if not self.target_ref:
            href = [v for k, v in attrs if k=='href']
            if href:
                #print href
                for item in href:
                    if item.startswith(self.pattern):
                        self.target_ref = item

    def handle_data(self, text):
        if (not self.is_done) and self.target_ref:
            self.dirs[text] = self.target_ref
            self.is_done = True


class URLLister2(SGMLParser):

    def __init__(self):
        SGMLParser.__init__(self)
        self.cur_ref = ""
        self.dirs = {}

    def start_a(self, attrs):
        if not self.cur_ref:
            href = [v for k, v in attrs if k=='href']
            if href:
                self.cur_ref = href[0]

    def end_a(self):
        self.cur_ref = ""

    def handle_data(self, text):
        if self.cur_ref:
            self.dirs[text] = self.cur_ref

build_url = 'http://autotest.datadirectnet.jp/results/'


def autotest_urlopen(url):
    req = urllib2.Request(url)
    base64string = \
        base64.encodestring('%s:%s' %
                            ('autotest', 'autotest4DdN')).replace('\n', '')
    req.add_header("Authorization", "Basic %s" % base64string)
    response = urllib2.urlopen(req)
    return response
try:
    pagehandle = autotest_urlopen(build_url)
    htmlsource = pagehandle.read()
    pagehandle.close()
except Exception, err:
    print str(err)
    exit(0)

parse = URLLister('879-')
parse.feed(htmlsource)

result_d = parse.target_ref
print parse.dirs
group_result_url = urlparse.urljoin(build_url, result_d)

print group_result_url
try:
    pagehandle = autotest_urlopen(group_result_url)
    htmlsource = pagehandle.read()
    pagehandle.close()
except Exception, err:
    print str(err)
    exit(0)

parse = URLLister2()

parse.feed(htmlsource)

print parse.dirs

for key, ref in parse.dirs.items():
    if key == ref:
        print urlparse.urljoin(group_result_url, ref)
#print parse.name




