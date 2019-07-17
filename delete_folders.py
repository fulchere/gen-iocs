import os
import shutil
names = open("folder_names", 'r')

for line in names:
    target = "../iocBoot/%s" % line[:-1]
    if os.path.isdir(target):
        shutil.rmtree(target)
if os.path.isfile('../Jenkinsfile'):
    os.remove('../Jenkinsfile')

print "Deleted all possible folders and single Jenkinsfile"
