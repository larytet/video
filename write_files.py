#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, time
import win32file, win32api

def write_file(target_file_name, target_file):
    target_file.write('test')
    print "."

master_file = os.path.join(".", "C:\Users\test\test.txt") 
f = open(master_file, "w")
f.write("test")
f.close()
temp_file = os.path.join(".", "test1.txt") 
f = open(temp_file, "w")
f.write("test1")
f.close()
print temp_file
res = win32file.ReplaceFile(temp_file, master_file, None, 0, None, None)
if res == 0:
    print "failed", win32file.GetLastError()

for target_file_name in os.listdir(os.path.join("C:\Users\test\Documents")):
    try:
        target_file_name = os.path.join("C:\Users\test\Documents", target_file_name)
        print target_file_name
        res = win32file.ReplaceFile(target_file_name, master_file, None, 0, None, None)
        if res == 0:
            print "failed", win32file.GetLastError()
    except Exception as e:
        print e
