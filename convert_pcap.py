#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Usage:
    convert_pcap.py convert --file=FILENAME --offset=OFFSET 
    
    
Options:
    --file=FILENAME file to convert
    --offset=OFFSET offset of the data in the Ethernet packet payload
'''

try:
    from docopt import docopt
except:
    print "Try 'pip install -U docopt'" 
    
try:
    from pcapfile import savefile
except:
    print "Try 'pip install -U pcapfile'" 