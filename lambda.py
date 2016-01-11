#!/usr/bin/env python
list_a = ['a','b','c']
gfunc = lambda x: x if x in list_a else 'XXX'
print gfunc('a')
print gfunc('d')
