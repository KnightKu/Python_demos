#!/usr/bin/env python
import jenkinsapi.api as Japi
import re

jenkin_url = "http://jenkins.datadirectnet.jp/"
jobid = "Autotest-lustre-hpdd"
job_lus='Gerrit-lustre-hpdd'
lus_id = 569
user = 'jenkins'
passwd = 'jenkins4DdN'
reg_exp = '(lustre-2.+\.x86_64\.rpm)'

#rets = Japi.search_artifact_by_regexp(jenkin_url, jobid, reg_exp, username=user, password=passwd)
rets = Japi.get_artifacts(jenkin_url, jobid, 834,username=user, password=passwd)
print rets
rets = Japi.get_artifacts(jenkin_url, job_lus, lus_id, username=user,password=passwd)
print rets

