# -*- coding: utf-8 -*
import time
import os
import threading

"""
För att inte skriva in lösen:
A ska logga in på B
A: ssh-keygen
välj var du vill spara nyckeln
tryck enter två ggr
ssh-copy-id -i nyckeln.pub username@backup_ip
"""

folder = ""
username = ""
backup_ip = ""
backup_folder = ""
time_between_backup = 3600

"""
--delete deletes files that don't exist on the system being backed up.(Optional)
-a preserves the date and times, and permissions of the files (same as -rlptgoD).
With -a option rsync will:
    Descend recursively into all directories (-r),
    copy symlinks as symlinks (-l),
    preserve file permissions (-p),
    preserve modification times (-t),
    preserve groups (-g),
    preserve file ownership (-o), and
    preserve devices as devices (-D). 
-z compresses the data
-vv increases the verbosity of the reporting process
-e specifies remote shell to use
"""
mega_str = "rsync -azvv -e ssh %s %s@%s:%s" % (folder, username, backup_ip, backup_folder)
print mega_str

try:
    while True:
        return_value = os.WEXITSTATUS(os.system(mega_str))
        # return_value kan vara 0 om den failar därför ska den inte användas
        time.sleep(time_between_backup)
except KeyBoardInterupt: 
    print "Avbryter backupen!"
