#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Usage:
    convert_pcap.py convert --file=FILENAME --offset=OFFSET 
    
    
Options:
    --file=FILENAME file to convert
    --offset=OFFSET offset of the data in the Ethernet packet payload
'''

import logging 
try:
    from docopt import docopt
except:
    print "Try 'pip install -U docopt'" 
    
try:
    from pcapfile import savefile
except:
    print "Try 'pip install -U pcapfile'" 
    
    
    
    
if __name__ == '__main__':
    pass
    arguments = docopt(__doc__, version='PCAP converter')
    logging.basicConfig()    
    logger = logging.getLogger('pcap')
    logger.setLevel(logging.INFO)    
    is_convert = arguments["convert"]
    filename = arguments["--file"]
    offset = arguments["--offset"]
    
    try:
        filecap = open(filename, 'rb')
    except:
        logger.error("Failed to open file '{0}' for reading".format(filename))
        exit(-1)
    
    packets = savefile.load_savefile(filecap, verbose=True).packets
    logger.info("Processing '{0}' packets".format(len(packets)))
