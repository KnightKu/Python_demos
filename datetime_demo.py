#!/usr/bin/env python
import datetime
import time

s_t = datetime.datetime.now()
delt = datetime.timedelta(minutes=2)
e_t = s_t + delt
while datetime.datetime.now() < e_t:
	time.sleep(10)
	print datetime.datetime.now()

