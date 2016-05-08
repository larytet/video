#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Write to all existing files in the Documents directory  

import os
import thread
import time


log_file_name = os.path.join(".", "write_files.log") 
log_file = open(log_file_name, "w");
target_folder = os.path.join(".", "Documents")
target_files = os.listdir(target_folder)
opened_files = []
def write_file(target_file_name, target_file):
    #log_file.write(filename+",")
    #log_file.flush()
    try:
        target_file.write('test')
        print "."
    except:
        pass

for target_file_name in target_files:
    try:
        target_file = open(target_file_name, "w")
        opened_files.append(target_file)  # keep the handler 
        thread.start_new_thread(write_file, (target_file_name, target_file,) )
    except:
        pass
time.sleep(100)
    

    