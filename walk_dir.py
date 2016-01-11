#!/usr/bin/env python
import os

for (dirpath, dirnames, filenames) in os.walk("/home/vms/"):
    for dirname in dirnames:  
        print('dirname = ' + dirname)  
    for filename in filenames:
        print('fileName = ' + filename)
