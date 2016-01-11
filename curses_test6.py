#!/usr/bin/python
#coding:utf-8

import curses, sys
import time,random
import threading

def workthread(stdscr,thno):
    speed=random.randint(100,200)/100.0
    testnumber=2
    for i in range(10):
        curprogress=0
        while (curprogress+speed*5)<100:
	    curprogress += speed*5
	    info='thread [%02d] is downloading... [%02d%%]     ' % (thno,curprogress)
	    updateprogress(stdscr,thno,info)
	    time.sleep(0.5)
        curprogress=100
        info='thread [%02d] is downloading... [%02d%%]     ' % (thno,curprogress)
        updateprogress(stdscr,thno,info)

def updateprogress(stdscr,line,info):
    stdscr.move(line,0)
    stdscr.addstr(line,0,info)
    stdscr.refresh()
    return 0

def main(stdscr):
    stdscr.clear()
    stdscr.refresh()

    #start thread
    threads={}
    threadnumbers=5
    for i in range(threadnumbers):
        th=threading.Thread(target=workthread,name='thread%d' % i,args=(stdscr,i))
        th.start()
        thid=str(th.ident)
        threads[thid]=th

    while 1:
        thidnume=[str(x.ident) for x in threading.enumerate()]
        for key,value in threads.items():
            if key not in thidnume:
	         threads.pop(key)
        if len(threads)<=0:
	    break
        time.sleep(1)

    return 0

curses.wrapper(main)
