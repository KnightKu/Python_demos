import fnmatch  
import os  
import re  
def fnmatch_filter_demo(path,pattern):  
    for path,dir,filelist in os.walk(path):  
        for name in fnmatch.filter(filelist,pattern):  
            print os.path.join(path,name)  
def fnmatch_demo(path,pattern):  
    for path,dir,filelist in os.walk(path):  
        for name in filelist:  
            if  fnmatch.fnmatch(name,pattern):  
                print os.path.join(path,name)  
def re_demo(path,pattern):  
    pattern=fnmatch.translate(pattern)  
    for path,dir,filelist in os.walk(path):  
        for name in filelist:  
            m=re.search(pattern,name)  
            if m:  
                print os.path.join(path,name)  
re_demo("/var/","*access*")
