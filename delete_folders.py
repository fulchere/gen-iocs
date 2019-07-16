import os
import shutil
names = open("folder_names", 'r')

for line in names:
    target = "../iocBoot/%s" % line[:-1]
    if os.path.isdir(target):
        shutil.rmtree(target)

print "Deleted all possible folders"
