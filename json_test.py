import json, logging, os

MSG = '{"project":"lustre-hpdd","branch":"b_ieel2_0_ddn","id":"I0152139e086135c0c0e428ca4af20072b91558b9","number":"657","subject":"LU-0000 test: gerrit test","owner":{"name":"Shuichi Ihara","email":"sihara@ddn.com","username":"sihara"},"url":"http://gerrit.datadirectnet.jp:8082/657","commitMessage":"LU-0000 test: gerrit test\n\nJust test.\n\nAUTOTEST:SKIP:sanity@lnet-selftest:1\n\nSigned-off-by: Shuichi Ihara \u003csihara@ddn.com\u003e\nChange-Id: I0152139e086135c0c0e428ca4af20072b91558b9\n","createdOn":1448962794,"lastUpdated":1448965865,"open":true,"status":"NEW"}'
#MSG='{"project":"lustre-hpdd","branch":"b_ieel2_0_ddn","id":"I0152139e086135c0c0e428ca4af20072b91558b9","number":"657","subject":"LU-0000 test: gerrit test","owner":{"name":"Shuichi Ihara","email":"sihara@ddn.com","username":"sihara"},"url":"http://gerrit.datadirectnet.jp:8082/657","commitMessage":"LU-0000 test: gerrit test Just test. Signed-off-by: Shuichi Ihara sihara@ddn.com Change-Id: I0152139e086135c0c0e428ca4af20072b91558b9","createdOn":1448962794,"lastUpdated":1448965865,"open":true,"status":"NEW"}'

MSG=MSG.strip('\n ').decode("unicode-escape")

MSG = MSG.replace('\n\n', '\\n\\n')
MSG = MSG.replace('\n', '\\n')
#print repr(MSG)
#print "-------------------"

#print str(MSG)

#print "-------------------"
#print str(repr(MSG))
#print "-------------------"
#r_MSG = repr(MSG)
#r_MSG = 
#dir_a = eval(MSG)


#print dir_a

lustre_exceptcases={}

j_obj = json.loads(MSG)

cmsg = json.dumps(j_obj['commitMessage']).replace('\\n\\n', '\n\n')
for line in cmsg.strip('\" ').splitlines():
    if line.strip().upper().startswith("AUTOTEST:"):
        logging.info(line)
        test_s = line.split("AUTOTEST:")[1].strip()
        if len(test_s) != 0:
            # Skip the autotest
            if test_s.upper() == "NONE":
                print("None!\n")
                #self.skip = True
                exit(0)
            elif test_s.upper().startswith("SKIP:"):
                print "Do skip!"
                skip_cases = test_s.split("SKIP:")[1]
                for item in skip_cases.strip().split('@'):
                    pair = item.strip().split(':')
                    if len(pair) == 1:
                        lustre_exceptcases[pair[0]] = "ALL"
                    elif len(pair) == 2:
                        lustre_exceptcases[pair[0]] = pair[1]
                    else:
                        logging.warning("Invalid AUTOTEST skip pattern!\n")
                        continue
            elif test_s.upper().startswith("ONLY:"):
                print("TOdo ONLY!")
                # TODO only
                exit(0)
            else:
                print("Not invalid!\n")
                exit()
print lustre_exceptcases
