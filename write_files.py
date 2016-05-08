#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, time
from itertools import count

def write_file(target_file_name, target_file):
    target_file.write('test')
    print "."

opened_files = []
count = 0
for target_file_name in os.listdir(os.path.join(".", "Documents")):
    count = count + 1
    if (count > 3):
        while (True):
            count = count + 1
    try:
        if count == 2:
            target_file_name = "test.txt"
        print target_file_name
        target_file = open(target_file_name, "w")
        opened_files.append(target_file)  # keep the handler 
        write_file(target_file_name, target_file)
    except:
        pass
time.sleep(10)
# close all handles, flush the data
for file_handle in opened_files:
    file_handle.close()

    