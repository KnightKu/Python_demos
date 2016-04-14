#!/usr/bin/env python
class test():
	def __init__(self):
		pass
	def printxxx(self, *osts):
		for item in osts:
			print item
		print min(osts)
	def prinxx(self):
		self.printxxx(1,2,3,4)

xtest = test()
xtest.prinxx()

