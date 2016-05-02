#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Usage:
    convert_pcap.py convert --filein=FILENAME --offset=OFFSET --fileout=FILENAME
    
    
Options:
    --filein=FILENAME file to convert
    --offset=OFFSET offset of the data in the Ethernet packet payload (HEX)
    --fileout=FILENAME file to generate
    
Example:
    ./convert_pcap.py convert --filein=udp.pcap --offset=30 --fileout=udp.pcap.bin
'''

import logging
from PIL import Image
 
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
    offset_str = arguments["--offset"]
    
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
        
    filename_image = filename_out+".png"
    
    offset = int(offset_str, 16)
    packets = savefile.load_savefile(filecap, verbose=True).packets
    logger.info("Processing '{0}' packets, data offset {1}".format(len(packets), hex(offset)))
    for packet in packets:
        packet_raw = packet.raw()
        fileout.write(packet_raw[offset:])
    fileout.close()
        
    img = Image.new('RGB', (640, 480))
    data = open(filename_out, 'rb').read()
    pixels = []
    count = len(data)
    while (count > 3):
        pixels.append(data[count:1], data[count:2], data[count:3])
        count = count - 3
    img.putdata(pixels)
    img.save(filename_image)