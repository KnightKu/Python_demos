#!/usr/bin/env python
import jenkins
import re


jenkin_url = "http://jenkins.datadirectnet.jp/"
jobid = "Autotest-lustre-hpdd"
user = 'jenkins'
passwd = 'jenkins4DdN'
reg_exp = '(lustre-2.+\.x86_64\.rpm)'

jen_server = jenkins.Jenkins(jenkin_url, username=user,password=passwd)

version = jen_server.get_version()

print version

jenkins.

#rets = Japi.search_artifact_by_regexp(jenkin_url, jobid, reg_exp, username=user, password=passwd)
rets = Japi.get_artifacts(jenkin_url, jobid, 834,username=user, password=passwd)
print rets


