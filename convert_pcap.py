#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Usage:
    convert_pcap.py convert --filein=FILENAME --offset=OFFSET --fileout=FILENAME
    
    
Options:
    --filein=FILENAME file to convert
    --offset=OFFSET offset of the data in the Ethernet packet payload
    --fileout=FILENAME file to generate
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
    filename = arguments["--filein"]
    filename_out = arguments["--fileout"]
    offset = arguments["--offset"]
    
    try:
        filecap = open(filename, 'rb')
    except:
        logger.error("Failed to open file '{0}' for reading".format(filename))
        exit(-1)

    try:
        fileout = open(filename_out, 'wb')
    except:
        logger.error("Failed to open file '{0}' for writing".format(filename_out))
        exit(-1)
    
    packets = savefile.load_savefile(filecap, verbose=True).packets
    logger.info("Processing '{0}' packets".format(len(packets)))
    for packet in packets:
        packet_raw = pkt.raw()
        fileout.write(packet_raw[:offset])
    fileout.close()
        
