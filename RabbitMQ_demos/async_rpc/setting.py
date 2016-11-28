#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'luotianshuai'

import os
import sys
import platform


if platform.system() == 'Windows':
    BASE_DIR = '\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])
    school_dbpaths = os.path.join(BASE_DIR,'school_db')

else:
    BASE_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
    school_dbpaths =os.path.join(BASE_DIR, 'school_db')


#rabbitmq服务地址ip
RabbitMQ_IP = 'localhost'
