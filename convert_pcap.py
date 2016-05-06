#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Get a recorded PCAP file, assume that payload is 16 bits RGB565, save the payload to the PNG image file 
# Data can come from OV7691 
'''
Usage:
    convert_pcap.py convert --filein=FILENAME --offset=OFFSET --fileout=FILENAME --resolution=WIDTH,HEIGHT
    convert_pcap.py udprx --fileout=FILENAME --port=UDP_PORT
    convert_pcap.py udptx --filein=FILENAME --port=UDP_PORT
    
    
Options:
    --filein=FILENAME file to convert
    --offset=OFFSET offset of the data in the Ethernet packet payload (HEX)
    --fileout=FILENAME file to generate
    --resolution=WIDTH,HEIGHT resolution of the image to process
    --port=UDP_PORT destination port for transmit, source port for recieve 
    
Example:
    ./convert_pcap.py convert --filein=udp.pcap --offset=0x30 --fileout=udp.pcap.bin
'''

import logging
try:
    from PIL import Image
except:
    print "Try 'pip install -U pillow'" 
     
try:
    from docopt import docopt
except:
    print "Try 'pip install -U docopt'" 
    
try:
    from pcapfile import savefile
except:
    print "Try 'pip install -U pypcapfile'" 
    

def openFile(filename, flag):
    '''
    Open a file for reading or writing
    Returns handle to the open file and result code False/True
    '''
    try:
        fileHandle = open(filename, flag) # read text file
    except Exception:
        logger.error('Failed to open file {0}'.format(filename))
        print sys.exc_info()
        return (False, None)
    else:
        return (True, fileHandle)
        
def get_mask(bits):
    return ((1 << bits) - 1)     


def get_bits(value, start, bits):
    mask = get_mask(bits)
    value = value >> start
    value = value & mask
    return value

def get_pixel_rgb565(data, index):
    rgb = (ord(data[index]) << 0) | (ord(data[index+1]) << 8)
    red = (get_bits(rgb, 11, 5) * 255)/31
    green = (get_bits(rgb, 5, 6) * 255)/63
    blue = (get_bits(rgb, 0, 5) * 255)/31
    return (red, green, blue)

def get_pixel_rgb565_1(data, index):
    rgb = (ord(data[index]) << 0) | (ord(data[index+1]) << 8)
    red = ((get_bits(rgb, 11, 5) * 527) + 23) >> 6  # r = ((((color >> 11) & 0x1F) * 527) + 23) >> 6;
    green = ((get_bits(rgb, 5, 6) * 259) + 33) >> 6 # g = ((((color >> 5) & 0x3F) * 259) + 33) >> 6;
    blue = ((get_bits(rgb, 0, 5) * 527) + 23) >> 6 # b = (((color & 0x1F) * 527) + 23) >> 6;
    return (red, green, blue)


def convert_image(arguments):
    while (True):
        filename_in = arguments["--filein"]
        filename_out = arguments["--fileout"]
        offset_str = arguments["--offset"]
        (result, filecap) = openFile(filename_in, 'rb')
        if (not result):
            logger.error("Failed to open file '{0}' for reading".format(filename))
            break

        (result, filecap) = openFile(filename_in, 'wb')
        if (not result):
            logger.error("Failed to open file '{0}' for writing".format(filename_out))
            break
        
if __name__ == '__main__':
    arguments = docopt(__doc__, version='PCAP converter')
    
    logging.basicConfig()    
    logger = logging.getLogger('pcap')
    logger.setLevel(logging.INFO)    
    
    is_convert = arguments["convert"]
    is_udprx = arguments["udprx"]
    is_udptx = arguments["udptx"]
    
    if (is_convert):
        convert_image(argumnets)
    if (is_udprx):
        run_udp_rx(argumnets)
    if (is_udptx):
        run_udptx(argumnets)
        
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
    img = Image.new('RGB', (320, 240), "black")
    data = open(filename_out, 'rb').read()
    pixels = []
    count = len(data)
    index = 0
    # I assume R5 G6 B5
    while (index < (count-2)):
        pixel = get_pixel_rgb565_1(data, index)
        pixels.append(pixel)
        index = index + 2
    img.putdata(pixels)
    img.save(filename_image)