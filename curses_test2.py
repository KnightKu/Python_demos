#!/usr/bin/env python
import curses
import time

def win_test():
    stdscr = curses.initscr()
    try:
        for i in range(10):
            (x, y) = stdscr.getmaxyx()

            stdscr.addstr(i,0,"X:%d, Y:%d" % (x,y))
            stdscr.refresh()
            time.sleep(1)
    finally:
       curses.endwin()

if __name__ == "__main__":
    win_test()
