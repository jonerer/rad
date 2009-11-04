#!/usr/bin/python2.5
from os.path import expanduser, join
import os, os.path, sys
import popen2

os.environ["PYTHONPATH"] =  os.environ["PYTHONPATH"] + ":" + join(expanduser("~"), "rad")

command = "run-standalone.sh python2.5 client/%s/main.py" % sys.argv[1]
print "Setting PYTHONPATH and running '%s'" % command
#os.system(path_command)
os.system(command)
