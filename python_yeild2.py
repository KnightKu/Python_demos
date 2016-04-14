# -*- coding:utf-8 -*-
# 生存全排列
def perm(items, n = None):
	if n is None:
		n = len(items)
	for i in range(len(items)):
		v = items[i:i+1]
		if n==1:
			yield v
		else:  
			rest = items[:i] + items[i+1:]
			for p in perm(rest, n-1):
				yield v + p
def comb(items, n = None):
	if n is None:
		n = len(items)
        else:
		for i in range(len(items)):
			v = items[i:i+1]
			if 1 == n:
				yield v
			else:
				rest = items[i+1:]
				for c in comb(rest, n-1):
					yield v + c
for item in perm([1,2,3,4]):
	print item

print "#######"
for item in comb([1]):
	print item
items = [1,2,3,4]
print items[1:]
