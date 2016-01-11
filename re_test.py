import re


for line in open("result.txt"):
	matchObj = re.match( r'(?p<title>^run_test) (?p<subtest>[a-zA-Z0-9]*) (?p<comment>\"([^"]+)\")', line, re.M|re.I)
	#matchObj = re.match( r'"(.*?)"', line, re.M|re.I)
	if matchObj:
		#print matchObj.group(0)
		#print matchObj.group(1)
		#print matchObj.group(2)
		#print matchObj.group(3)
		print matchObj.groups()['subtest']
		print matchObj.groups()['comment']

