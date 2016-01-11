#!/usr/bin/python
'''an example for generate html page.
the module used is:PyH
Its home page is: http://code.google.com/p/pyh/
we can download it at:http://code.google.com/p/pyh/downloads/detail?name=PyH-0.1.1.tar.gz&can=2&q=
More things about html at:http://www.w3school.com.cn/tags/tag_div.asp
'''
from sys import _getframe, stdout, modules, version
nOpen={}

nl = '\n'
doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n'
charset = '<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />\n'

tags = ['html', 'body', 'head', 'link', 'meta', 'div', 'p', 'form', 'legend', 
        'input', 'select', 'span', 'b', 'i', 'option', 'img', 'script',
        'table', 'tr', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'fieldset', 'a', 'title', 'body', 'head', 'title', 'script', 'br', 'table',
        'ul', 'li', 'ol']

selfClose = ['input', 'img', 'link', 'br']

class Tag(list):
    tagname = ''
    
    def __init__(self, *arg, **kw):
        self.attributes = kw
        if self.tagname : 
            name = self.tagname
            self.isSeq = False
        else: 
            name = 'sequence'
            self.isSeq = True
        self.id = kw.get('id', name)
        #self.extend(arg)
        for a in arg: self.addObj(a)

    def __iadd__(self, obj):
        if isinstance(obj, Tag) and obj.isSeq:
            for o in obj: self.addObj(o)
        else: self.addObj(obj)
        return self
    
    def addObj(self, obj):
        if not isinstance(obj, Tag): obj = str(obj)
        id=self.setID(obj)
        setattr(self, id, obj)
        self.append(obj)

    def setID(self, obj):
        if isinstance(obj, Tag):
            id = obj.id
            n = len([t for t in self if isinstance(t, Tag) and t.id.startswith(id)])
        else:
            id = 'content'
            n = len([t for t in self if not isinstance(t, Tag)])
        if n: id = '%s_%03i' % (id, n)
        if isinstance(obj, Tag): obj.id = id
        return id

    def __add__(self, obj):
        if self.tagname: return Tag(self, obj)
        self.addObj(obj)
        return self

    def __lshift__(self, obj):
        self += obj
        if isinstance(obj, Tag): return obj

    def render(self):
        result = ''
        if self.tagname:
            result = '<%s%s%s>' % (self.tagname, self.renderAtt(), self.selfClose()*' /')
        if not self.selfClose():
            for c in self:
                if isinstance(c, Tag):
                    result += c.render()
                else: result += c
            if self.tagname: 
                result += '</%s>' % self.tagname
        result += '\n'
        return result

    def renderAtt(self):
        result = ''
        for n, v in self.attributes.iteritems():
            if n != 'txt' and n != 'open':
                if n == 'cl': n = 'class'
                result += ' %s="%s"' % (n, v)
        return result

    def selfClose(self):
        return self.tagname in selfClose        
    
def TagFactory(name):
    class f(Tag):
        tagname = name
    f.__name__ = name
    return f

thisModule = modules[__name__]

for t in tags: setattr(thisModule, t, TagFactory(t)) 

def ValidW3C():
    out = a(img(src='http://www.w3.org/Icons/valid-xhtml10', alt='Valid XHTML 1.0 Strict'), href='http://validator.w3.org/check?uri=referer')
    return out

class PyH(Tag):
    tagname = 'html'
    
    def __init__(self, name='MyPyHPage'):
        self += head()
        self += body()
        self.attributes = dict(xmlns='http://www.w3.org/1999/xhtml', lang='en')
        self.head += title(name)

    def __iadd__(self, obj):
        if isinstance(obj, head) or isinstance(obj, body): self.addObj(obj)
        elif isinstance(obj, meta) or isinstance(obj, link): self.head += obj
        else:
            self.body += obj
            id=self.setID(obj)
            setattr(self, id, obj)
        return self

    def addJS(self, *arg):
        for f in arg: self.head += script(type='text/javascript', src=f)

    def addCSS(self, *arg):
        for f in arg: self.head += link(rel='stylesheet', type='text/css', href=f)
    
    def printOut(self,file=''):
        if file: f = open(file, 'w')
        else: f = stdout
        f.write(doctype)
        f.write(self.render())
        f.flush()
        if file: f.close()

page = PyH("MyPage")
#page.addCSS('myStylesheet1.css', 'myStylesheet2.css')
#page.addJS('myJavascript1.js', 'myJavascript2.js')

badu="http://www.baidu.com"
#<h1 align="center">MyTitle1</h1>
page <<a(badu,href=badu)
page <<h1('MyTitle1',align='center')

#<div align="center" id="myDiv1"><p id="myp1">my paragraph1</p>
#</div>
page << div(align='center',id='myDiv1') << p('my paragraph1',id='myp1')

#<div id="myDiv2"><h2>title2 in div2<p>paragraph under title2</p>
#</h2>
#</div>
mydiv2 = page << div(id='myDiv2')
mydiv2 << h2('title2 in div2') << p('paragraph under title2')

#<div align="right" id="myDiv3"><p>paragraph in mydiv3</p>
#</div>
mydiv3 = page << div(id='myDiv3')

#<table border="1" id="mytable1"><tr id="headline"><td>Head1<td>Head2</td>
#</td>
#</tr>
#<tr id="line1"><td>r1,c1<td>r1,c2</td>
#</td>
#</tr>
#<tr id="line2"><td>r2,c1<td>r2,c2</td>
#</td>
#</tr>
#</table>
table1 = page << table(border='1',id='mytable1')
headtr = table1 << tr(id='headasdasdline')
headtr << td('Test_Suite') << td('Status') << td('Total') << td('Pass') << td('Fail') << td('Skip',width=400, style="word-break:break-all")

tr1 = table1 << tr(id='lineasd1')
status = "PASS"
tr1 << td('sanity') << td(status, bgcolor= 'red' if status == 'PASS' else 'yellow') << td('100') <<td('20') << td('10') << td('10')
tr2 = table1 << tr(id='linesda2')
tr2 << td('') << td('') << td('') << td('') << td('') << td('ALWAYS:<br> 2')
tr3 = table1 << tr(id='lineasda3')
tr3 << td('') << td('') << td('') << td('') << td('') << td('SLOW: 222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222')
tr4 = table1 << tr(id='lineasd4')
tr4 << td('') << td('') << td('') << td('') << td('') << td('MANUAL: 2')
tr5 = table1 << tr(id='linsdasde5')
tr5 << td('') << td('') << td('') << td('') << td('') << td('OTHERS', bgcolor="red" if 0 else "green")
print "+++++"
del tr5[:]
print "-----"
del table1[:]
page << p(id='22')
page << p(id='33')
page << p(id='44')

page << a("badu",href=badu)
page << br()
page << a("badu",href=badu)
page << a("badu",href=badu)
page << a("badu",href=badu)
page << a("badu",href=badu)
page << i("Status: Failed (Failed to start or aborted)")
table2 = page << table(border='1',id='mytable2')
headtr2 = table2 << tr(id='headline')
headtr2 << td('Head1') << td('Head2') << td('Head3') << td('Head4')

tr1 = table2 << tr(id='line1')
tr1 << td('r1,c1') << td('r1,c2') << td('') << td('r1,c2, 444')

tr2 = table2 << tr(id='line2')
tr2 << td('www.baidu.com') << td('r2,c2')

for i in range(10):
	tr2 = table2 << tr(id='line3')
	tr2 << td('www.baidu.com') << td('r2,c2') << td('') << td('r1,c2, 444') << td('') << td('r1,c2, 444')

tr6 = table1 << tr(id='line6')
tr6 << td(123123) << td('B') << td('C') << td('D') << td('E') << td('F')

"""
tr1 = table1 << tr(id='lineasd1')
status = "PASS"
tr1 << td('sanity') << td(status, bgcolor= 'red' if status == 'PASS' else 'yellow') << td('100') <<td('20') << td('10') << td('10')
tr2 = table1 << tr(id='linesda2')
tr2 << td('') << td('') << td('') << td('') << td('') << td('ALWAYS:<br> 2')
tr3 = table1 << tr(id='lineasda3')
tr3 << td('') << td('') << td('') << td('') << td('') << td('SLOW: 222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222')
tr4 = table1 << tr(id='lineasd4')
tr4 << td('') << td('') << td('') << td('') << td('') << td('MANUAL: 2')
tr5 = table1 << tr(id='linsdasde5')
tr5 << td('') << td('') << td('') << td('') << td('') << td('OTHERS', bgcolor="red" if 0 else "green")
tr5 << td('') << td('') << td('') << td('') << td('') << td('OTHERS', bgcolor="red" if 0 else "green")
"""
#The result is:
#<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
#<html lang="en" xmlns="http://www.w3.org/1999/xhtml"><head><title>MyPage</title>
#</head>
#<body><h1 align="center">MyTitle1</h1>
#<div align="center" id="myDiv1"><p id="myp1">my paragraph1</p>
#</div>
#<div id="myDiv2"><h2>title2 in div2<p>paragraph under title2</p>
#</h2>
#</div>
#<div align="right" id="myDiv3"><p>paragraph in mydiv3</p>
#</div>
#<table border="1" id="mytable1"><tr id="headline"><td>Head1<td>Head2</td>
#</td>
#</tr>
#<tr id="line1"><td>r1,c1<td>r1,c2</td>
#</td>
#</tr>
#<tr id="line2"><td>r2,c1<td>r2,c2</td>
#</td>
#</tr>
#</table>
#</body>
#</html>
page.printOut()
