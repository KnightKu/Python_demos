import HTMLParser
import urlparse
import re
import urllib2, urllib


build_url = "http://mirror.centos.org/centos/6/updates/x86_64/Packages/"


class my_parse(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.rpm_name = ""

    def handle_data(self, data):
        match = re.search('(kernel-2.+\.x86_64\.rpm)', data)
        if match:
            self.rpm_name = match.group(1)
            return


def autotest_urlopen(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    return response

try:
    pagehandle = autotest_urlopen(build_url)
    htmlsource = pagehandle.read()
    pagehandle.close()
    parse = my_parse()
    parse.feed(htmlsource)
    rpm_url = urlparse.urljoin(build_url, parse.rpm_name)
    print rpm_url
    urllib.urlretrieve(rpm_url)
except Exception, err:
    print str(err)
    exit(0)