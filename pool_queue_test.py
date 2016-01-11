#!/usr/bin/env python

from time import sleep,ctime
import thread

sign=[False,False,False]
listA=[1,2,3,4,5,6]

lock = thread.allocate_lock()
def loop0(index, i):
	print  index
	sleep(2)

        if lock.acquire():
		sign[i]=False
		lock.release()

def main():
	for item in listA:
	#	print item
		while 1:
			create = False
	#		print "start craet"
			for i in range(len(sign)):
	#			print "XXXXXXXXXXX"
				if not sign[i]:
					sign[i]=True
					thread.start_new_thread(loop0,(item,i))
					create = True
					break
			if create:
				break
	sleep(10)
	print sign
#    while not all(sign):pass
 #   print 'all DONE at:',ctime()
 
if __name__=='__main__':
    main()


