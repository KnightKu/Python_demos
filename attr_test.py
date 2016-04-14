class control_conf:
    autotest_web = ''
    jenkins_at_job_name = ''
    jenkins_at_build_num = ''
    jenkins_build_number = ''
    jenkins_job_name = ''
    gerrit_change_number = ''
    gerrit_patchset_number = ''
    jenkins_job_url = ''
    jenkins_username = ''
    jenkins_password = ''

    def __init__(self):
        self.att1 = '2'
	self.att2 = '3'

    def func(self, foo, foo1, fooo2):
        print self.__dict__
ctl = control_conf()
ctl2 = control_conf()
ctl2.att2='4'
ctl.func('xx',
#asdasdasd
	'xzxc',
#asdasdasd
'asd')
