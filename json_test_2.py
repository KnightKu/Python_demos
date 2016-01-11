import json, logging, os

cmd = "ssh -p 29418 autotest@10.128.7.3 gerrit query change:622 --format=JSON | awk 'NR==1 {print}'"

MSG=os.popen(cmd).read()

print MSG

#j_obj = json.loads(MSG)

MSG=MSG.strip('\n')
MSG=MSG.decode("unicode-escape")

"""
with open("/tmp/test_json.json", 'rw+') as fd:
        fd.write(MSG.decode("unicode-escape"))
"""

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


print MSG

lustre_exceptcases={}

j_obj = json.loads(MSG)

cmsg = json.dumps(j_obj['commitMessage']).replace('\\n\\n', '\n\n')
print cmsg
for line in cmsg.strip('\" ').splitlines():
        if line.strip().startswith("AUTOTEST:"):
                print line
                test_s = line.split("AUTOTEST:")[1].strip()
                print test_s
                if len(test_s) != 0:
                        for item in test_s.strip().split('@'):
                                pair = item.strip().split(':')
                                if len(pair) != 2:
                                        logging.warning("Invalid skip pattern:%s                                                                                                                " % item)
                                        continue
                                lustre_exceptcases[pair[0]] = pair[1]
print lustre_exceptcases

