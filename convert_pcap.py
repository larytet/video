#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Get a recorded PCAP file, assume that payload is 16 bits RGB565, save the payload to the PNG image file 
# Data can come from OV7691 
'''
Usage:
    convert_pcap.py convert --filein=FILENAME --offset=OFFSET --fileout=FILENAME --resolution=WIDTH,HEIGHT
    convert_pcap.py udprx --fileout=FILENAME --port=UDP_PORT --resolution=WIDTH,HEIGHT
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

import sys
import logging
import re
import socket
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
    
def convert_to_int(s, base):
    value = None;
    try:
        value = int(s, base);
        result = True;
    except:
        logger.error("Bad formed number '{0}'".format(s));
        result = False;
    return (result, value);

def open_file(filename, flag):
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


def parse_arguments_resolution(resolution_arg):
    pattern = "([0-9]+).([0-9]+)"
    m = re.match(pattern, resolution_arg)
    result = (m is not None)
    
    if (result):
        (_, width) = convert_to_int(m.group(1), 10)
        (_, height) = convert_to_int(m.group(2), 10)
        return (result, width, height)
    logger.error("Failed to parse image resolution '{0}' ".format(resolution_arg))
    return (result, None, None)
    
def convert_image(arguments):
    while (True):
        filename_in = arguments["--filein"]
        filename_out = arguments["--fileout"]
        offset_str = arguments["--offset"]
        (result, filecap) = open_file(filename_in, 'rb')
        if (not result):
            logger.error("Failed to open file '{0}' for reading".format(filename_in))
            break

        (result, fileout) = open_file(filename_out, 'wb')
        if (not result):
            logger.error("Failed to open file '{0}' for writing".format(filename_out))
            break


        (result, width, height) = parse_arguments_resolution(arguments["--resolution"])
        if (not result):
            break
            
        filename_image = filename_out+".png"
    
        # Read the PCAP file , save the payload in a separate file
        offset = int(offset_str, 16)
        packets = savefile.load_savefile(filecap, verbose=True).packets
        logger.info("Processing '{0}' packets, data offset {1}, resolution {2}x{3}".format(len(packets), hex(offset), width, height))
        for packet in packets:
            packet_raw = packet.raw()
            fileout.write(packet_raw[offset:])
        fileout.close()
        
        # Generate am image file 
        img = Image.new('RGB', (width, height), "black")
        data = open(filename_out, 'rb').read()
        pixels = []
        count = len(data)
        expected_count = width * height
        index = 0
        # I assume R5 G6 B5
        while (index < (count-2)):
            pixel = get_pixel_rgb565_1(data, index)
            pixels.append(pixel)
            index = index + 2
            if (len(pixels) >= expected_count):
                if (index < (count-2)):
                    logger.warning("Too much data for the image {0}x{1}. Expected {2} pixels, got {3} pixels".format(width, height, expected_count, count/2))
                break;
            
        if (len(pixels) < expected_count):
            logger.warning("Not enough data for the image {0}x{1}. Expected {2} pixels, got {3} pixels".format(width, height, expected_count, len(pixels)))
        img.putdata(pixels)
        img.save(filename_image)
        logger.warning("Generated file {0}".format(filename_image))
                    
        break;
    
def run_udp_rx_thread(filename_base, udp_socket, width, heigh):
    frame_index = 0            
    filename_image = "{0}.{1}.rgb565".format(filename_base, frame_index))
        
        
    
def run_udp_rx(arguments):    
    while (True):
        filename_out = arguments["--fileout"]
        (result, fileout) = open_file(filename_out, 'wb')
        if (not result):
            logger.error("Failed to open file '{0}' for writing".format(filename_out))
            break
        
        (result, width, height) = parse_arguments_resolution(arguments["--resolution"])
        if (not result):
            break
        
        udp_port_str = arguments["--port"]
        (result, udp_port) = convert_to_int(udp_port_str, 10)
        if (not result):
            logger.error("Failed to parse UDP port number '{0}'".format(udp_port_str))
            break;

        try:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(("127.0.0.1", udp_port))
        except Exception as e:
            logger.error("Failed to bind UDP port {0}. Probably is bound by different application".format(udp_port))
            logger.error(e.to_str())
            break
        
        run_udp_rx_thread(filename_out, udp_socket, widht, height)
        
        break

def run_udp_tx(arguments):
    while (True):    
        filename_out = arguments["--fileout"]
        (result, fileout) = open_file(filename_out, 'wb')
        if (not result):
            logger.error("Failed to open file '{0}' for writing".format(filename_out))
            break
        
        (result, width, height) = parse_arguments_resolution(arguments["--resolution"])
        if (not result):
            break
            
        filename_image = filename_out+".png"
        
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
        convert_image(arguments)
    elif (is_udprx):
        run_udp_rx(arguments)
    elif (is_udptx):
        run_udptx(arguments)
        
