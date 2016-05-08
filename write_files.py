#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time

def write_file(target_file_name, target_file):
    try:
        target_file.write('test')
        print "."
    except:
        pass

opened_files = []
for target_file_name in os.listdir(os.path.join(".", "Documents")):
    try:
        target_file = open(target_file_name, "w")
        opened_files.append(target_file)  # keep the handler 
        write_file(target_file_name, target_file)
    except:
        pass
time.sleep(10)
# close all handles, flush the data
for file_handle in opened_files:
    file_handle.close()

    