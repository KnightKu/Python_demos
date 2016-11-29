#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import os
import platform


#添加BASE_DIR,添加顶级目录到路径中,方便调用其他目录模块
if platform.system() == 'Windows':
    print(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])
    BASE_DIR = '\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])
else:
    BASE_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])


#加载环境变量
sys.path.append(BASE_DIR)
import main

if __name__ == '__main__':
    obj = main.Handler()
    obj.start()

