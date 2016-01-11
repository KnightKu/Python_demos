#!/usr/bin/env python
import curses
import time

def print_curse():
        # Initialize curses
        stdscr=curses.initscr()
        print "a"
        try:
            i = 0
            while i < 10:
                stdscr.addstr(i, 0, "I am line %d" % i)
                i += 1
            stdscr.clear()
            time.sleep(2)
            i = 0
            while i < 10:
                stdscr.addstr(i, 0, "I am line %d" % i)
                i += 1
        except:
           raise
        curses.endwin() # Terminate curses
if __name__ == "__main__":
    print_curse()
