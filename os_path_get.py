import os,os.path
def VisitDir(arg,dirname,names):
  for filespath in names:
    if filespath.startswith('Result_summary'):
        print os.path.join(dirname,filespath)
def Getsubpath(path):
    for (dirpath, dnames, fnames) in os.walk(path):
        for dname in dnames:
            if dname.startswith('879-'):
                return os.path.join(path,dname)
    return ''
if __name__=="__main__":


    path="/usr/local/autotest/results/"
    subpath = Getsubpath(path)


    os.path.walk(subpath,VisitDir,())

