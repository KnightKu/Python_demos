#!/usr/bin/env python
import threading,time
import fcntl
pid_file ='/tmp/program.pid'
fp = 0

def dummy_lock():
    print "Opening file...",pid_file
    fp = open(pid_file,'r+')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
        print "Accessed the lock..."
    except IOError:
        fp.close()
        # another instance is running
        return False
    return True

def dummy_unlock():
    if fp == 0:
        return
    fcntl.lockf(fp, fcntl.LOCK_UN)

def mythread():
	global a
	if dummy_lock():      #acquire the lock
		a=threading.currentThread().getName()
		time.sleep(20)
		print "a is modified by",a
		dummy_unlock()      #release the lock
	else:
		print "Failed access lock"
mythread()
