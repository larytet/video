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
    print target_file_name
    #log_file.write(filename+",")
    #log_file.flush()
    target_file.write('test')

for target_file_name in target_files:
    target_file = open(target_file_name, "w")
    opened_files.append(target_file)  # keep the handler 
    thread.start_new_thread(write_file, (target_file_name, target_file,) )
time.sleep(100)
    

    