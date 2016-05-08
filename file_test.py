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

def write_file(filename):
    print filename
    time.sleep(1)
    log_file.write(filename+",")
    target_file = open(target_file_name, "w")
    target_file.write('test')
    log_file.flush()

for target_file_name in target_files:
    thread.start_new_thread(write_file, (target_file_name,) )
    time.sleep(100)
    

    