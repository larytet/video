#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, time
import win32file, win32api

def write_file(target_file_name, target_file):
    target_file.write('test')
    print "."

master_file = os.path.join(".", "test.txt") 
f = open(master_file, "w")
f.write("test")
f.close()
temp_file = os.path.join(".", "test1.txt") 
f = open(temp_file, "w")
f.write("test1")
f.close()
print temp_file
win32file.ReplaceFile("test1.txt", "test.txt", "test2.txt", 0, NULL, NULL)

opened_files = []
for target_file_name in os.listdir(os.path.join(".", "Documents")):
    try:
        print target_file_name
        win32file.ReplaceFile(target_file_name, master_file, NULL, 0, NULL, NULL)
    except Exception as e:
        pass
time.sleep(10)
# close all handles, flush the data
for file_handle in opened_files:
    file_handle.close()

    