#!/usr/bin/env python
import threading,time
q=threading.Lock()   #create a lock object
def mythread():
	global a
	q.acquire()      #acquire the lock
	a=threading.currentThread().getName()
	print "a is modified by",a
	q.release()      #release the lock
	
for i in range(1,4):
	t=threading.Thread(target=mythread,name="Thread %d"%i)
	t.start()
