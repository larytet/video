#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Get a recorded PCAP file, assume that payload is 24 bits RGB, save the payload to the PNG image file 
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
    
    
def get_mask(bits):
    return ((1 << bits) - 1)     


def get_bits(value, start, bits):
    mask = get_mask(bits)
    value = value >> start
    value = value & mask
    return value

def get_pixel_rgb565(data, index):
    rgb = (ord(data[index]) << 0) | (ord(data[index+1]) << 8)
    red = get_bits(rgb, 11, 5) * (255/32)
    green = get_bits(rgb, 5, 6) * (255/64)
    blue = get_bits(rgb, 0, 5) * (255/32)
    return (red, green, blue)

    
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
    
    # Read the PCAP file , save the payload in a separate file
    offset = int(offset_str, 16)
    packets = savefile.load_savefile(filecap, verbose=True).packets
    logger.info("Processing '{0}' packets, data offset {1}".format(len(packets), hex(offset)))
    for packet in packets:
        packet_raw = packet.raw()
        fileout.write(packet_raw[offset:])
    fileout.close()
        
    # Generate am image file 
    img = Image.new('RGB', (320, 240))
    data = open(filename_out, 'rb').read()
    pixels = []
    count = len(data)
    index = 0
    # I assume R5 G6 B5
    while (index < (count-2)):
        pixel = get_pixel_rgb565(data, index)
        pixels.append(pixel)
        index = index + 2
    img.putdata(pixels)
    img.save(filename_image)