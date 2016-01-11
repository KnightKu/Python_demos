#!/usr/bin/env python

import yaml

dictA = {'A': 2, 'B': 3}
dictB = {'C': 2, 'D': 3}
dictC = {'F': 2, 'E': 3}
dictD = {'G': 2, 'H': 3}
dictX = {'1': dictA, 4: dictB, '3': dictC, '23': dictD}
print sorted(dictX.keys(), key=int)
print dictX
print dictX.values()

#dictX={'host': {'ip01': {'two': '192.168.1.254', 'one': '192.168.1.2'}, 'ip00': '192.168.1.1'}, 'soft': {'apache': 2.2, 'php': 5.3, 'mysql': 5.2}}

#print dictX

file = '/tmp/test.yml'
f=open(file,'w')
yaml.dump(dictX,f, default_flow_style=False)
f.close()

f = open(file)
for line in f:
	print line
f.close()
