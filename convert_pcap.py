#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Get a recorded PCAP file, assume that payload is 16 bits RGB565, save the payload to the PNG image file
# Data can come from OV7691
'''
Usage:
    convert_pcap.py convert --filein=FILENAME --offset=OFFSET --fileout=FILENAME --resolution=WIDTH,HEIGHT
    convert_pcap.py udprx --fileout=FILENAME --port=UDP_PORT --resolution=WIDTH,HEIGHT  [--ffmpeg=FFMPEG_PATH]
    convert_pcap.py udptx --filein=FILENAME --port=UDP_PORT --ip=IP_ADDRESS --rate=FRAME_RATE
    convert_pcap.py udprxsim --port=UDP_PORT --resolution=WIDTH,HEIGHT


Options:
    --filein=FILENAME file to convert
    --offset=OFFSET offset of the data in the Ethernet packet payload (HEX)
    --fileout=FILENAME file to generate
    --resolution=WIDTH,HEIGHT resolution of the image to process
    --port=UDP_PORT destination port for transmit, source port for receive
    --ip=IP_ADDRESS destination IP address
    --rate=FRAME_RATE maximum frame rate for transmit in frames per second
    --ffmpeg=FFMPEG_PATH full file path to the ffmpeg utility, if specified receive will generate PNG files instead of RGB565 files  

Example:
    ./convert_pcap.py convert --filein=udp.pcap --offset=0x30 --fileout=udp.pcap.bin
'''

import logging
import re
import socket
import struct
import time
import thread
import threading
from datetime import datetime
import subprocess

try:
    from PIL import Image
except Exception as e:
    print "Try 'pip install -U pillow'"
    print e

try:
    from docopt import docopt
except Exception as e:
    print "Try 'pip install -U docopt'"
    print e

try:
    from pcapfile import savefile
except Exception as e:
    print "Try 'pip install -U pypcapfile'"
    print e

def convert_to_int(str, base):
    value = None
    try:
        value = int(str, base)
        result = True
    except Exception as e:
        logger.error("Bad formed number '{0}'".format(str))
        logger.error(e)
        result = False
    return (result, value)

def open_file(filename, flag):
    '''
    Open a file for reading or writing
    Returns handle to the open file and result code False/True
    '''
    try:
        file_handle = open(filename, flag) # read text file
    except Exception as e:
        logger.error('Failed to open file {0}'.format(filename))
        logger.error(e)
        return (False, None)
    else:
        return (True, file_handle)

def get_mask(bits):
    return (1 << bits) - 1


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
    red = ((get_bits(rgb, 11, 5) * 527) + 23) >> 6
    green = ((get_bits(rgb, 5, 6) * 259) + 33) >> 6
    blue = ((get_bits(rgb, 0, 5) * 527) + 23) >> 6
    return (red, green, blue)


def parse_arguments_resolution(resolution_arg):
    pattern = "([0-9]+).([0-9]+)"
    re_match = re.match(pattern, resolution_arg)
    result = (re_match is not None)

    if result:
        (_, width) = convert_to_int(re_match.group(1), 10)
        (_, height) = convert_to_int(re_match.group(2), 10)
        return (result, width, height)
    logger.error("Failed to parse image resolution '{0}' ".format(resolution_arg))
    return (result, None, None)

def parse_arguments_ffmpeg(arguments):
    result = False
    ffmpeg_path = None
    while True:
        if not arguments["--ffmpeg"]:
            break
        
        ffmpeg_path = arguments["--ffmpeg"]
        ffmpeg_output = []
        try:
            process = subprocess.Popen([ffmpeg_path, "-h"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            (ffmpeg_output, err) = process.communicate()
            exit_code = process.wait()
        except Exception as e:
            logger.error(e)
        result = "version" in ffmpeg_output
        if not result:
            logger.warning("Failed to run '{0}'".format(ffmpeg_path))
            break
        break

    if not result:
        logger.warning("No ffmpeg path is specified. Storing raw image files")
    
    return (result, ffmpeg_path)

FRAME_INDEX_OFFSET = 0 # bytes
FRAME_INDEX_SIZE = 2 # bytes

FRAGMENT_INDEX_OFFSET = FRAME_INDEX_OFFSET+FRAME_INDEX_SIZE
FRAGMENT_INDEX_SIZE = 4 # bytes

HEADER_SIZE = FRAGMENT_INDEX_SIZE + FRAME_INDEX_SIZE


def convert_image(arguments):
    while True:
        filename_in = arguments["--filein"]
        filename_out = arguments["--fileout"]
        offset_str = arguments["--offset"]
        (result, filecap) = open_file(filename_in, 'rb')
        if not result:
            logger.error("Failed to open file '{0}' for reading".format(filename_in))
            break

        (result, fileout) = open_file(filename_out, 'wb')
        if not result:
            logger.error("Failed to open file '{0}' for writing".format(filename_out))
            break


        (result, width, height) = parse_arguments_resolution(arguments["--resolution"])
        if not result:
            break

        filename_image = filename_out+".png"

        # Read the PCAP file , save the payload (RGB565) in a separate file
        offset = int(offset_str, 16)
        packets = savefile.load_savefile(filecap, verbose=True).packets
        logger.info("Processing '{0}' packets, data offset {1}, resolution {2}x{3}".format(
            len(packets), hex(offset), width, height))
        for packet in packets:
            packet_raw = packet.raw()
            #frame_index = struct.unpack('<I', data[FRAME_INDEX_OFFSET:FRAME_INDEX_OFFSET+FRAME_INDEX_SIZE])
            #fragment_index = struct.unpack('<I', data[FRAGMENT_INDEX_OFFSET:FRAGMENT_INDEX_OFFSET+FRAGMENT_INDEX_SIZE])
            fileout.write(packet_raw[offset:])
        fileout.close()
        logger.info("Generated file {0}".format(filename_out))

        # Generate am image file
        img = Image.new('RGB', (width, height), "black")
        data = open(filename_out, 'rb').read() # read the RGB565 data from the filename_out 
        pixels = []
        count = len(data)
        expected_count = width * height
        index = 0
        # I assume R5 G6 B5
        while index <= (count-2):
            pixel = get_pixel_rgb565_1(data, index)
            pixels.append(pixel)
            index = index + 2
            if len(pixels) >= expected_count:
                if index < (count-2):
                    logger.warning("Too much data for the image {0}x{1}. Expected {2} pixels, got {3} pixels".format(
                        width, height, expected_count, count/2))
                break

        if len(pixels) < expected_count:
            logger.warning("Not enough data for the image {0}x{1}. Expected {2} pixels, got {3} pixels".format(
                width, height, expected_count, len(pixels)))
        img.putdata(pixels)
        img.save(filename_image)
        logger.info("Generated file {0}".format(filename_image))

        break
    
def save_frame_to_file(filename_base, addr, frame, frame_index, ffmpeg_path):
    if ffmpeg_path == None:
        filename_image = "{0}.{1}.{2}.rgb565".format(filename_base, addr, frame_index)
        (result, fileout) = open_file(filename_image, "wb")
        if (result):
            fileout.write(frame)
            fileout.close()
            #logger.info("Generated file {0}".format(filename_image))
        else:
            logger.warning("Failed to open file {0} for writing, drop frame {1}".format(
                filename_image, frame_index))
    else:
        filename_image = "{0}.{1}.{2}.png".format(filename_base, addr, frame_index)
    
def run_udp_rx_simulation(udp_socket, width, height):
    expected_frame_size = width * height * 2

    # Dictionary of the received UDP packets. The key is source IP address
    received_udp_packets = {}
    rx_buffer_size = 1500
    received_bytes = 0
    while True:
        try:
            data, addr = udp_socket.recvfrom(rx_buffer_size)
        except Exception as e:
            logger.error("Failed to read UDP socket")
            logger.error(e)
            break
        received_bytes = received_bytes + len(data)
        if (len(data) < 1300):
            logger.error("Frame completed {0} bytes".format(received_bytes))
            received_bytes = 0
            
        
def run_udp_disconnected_clients(received_udp_packets, lock):
    '''
    Wake up periodically, check the latest time stamp in the dictionary
    if there is no data for some time declare the client disconnected
    '''
    while True:
        time.sleep(1.0)
        timestamp = time.time()
        disconnected_clients = []
        with lock:
            for addr in received_udp_packets:
                (_, received_frames, _, _, last_timestamp) = received_udp_packets[addr]
                if (timestamp - last_timestamp) > 1.0:
                    disconnected_clients.append((addr, received_frames))
        for (addr, received_frames) in disconnected_clients:
            with lock:
                del received_udp_packets[addr]
            logger.info("{0} Client {1} disconnected after {2} frames".format(datetime.now(), addr, received_frames))
            
    
def run_udp_rx_thread(filename_base, udp_socket, width, height, ffmpeg_path):
    expected_frame_size = width * height * 2

    # Dictionary of the received UDP packets. The key is source IP address
    received_udp_packets = {}
    lock = lock = threading.Lock()
    thread.start_new_thread(run_udp_disconnected_clients, (received_udp_packets, lock))
    rx_buffer_size = 1500
    while True:
        try:
            data, addr = udp_socket.recvfrom(rx_buffer_size)
        except Exception as e:
            logger.error("Failed to read UDP socket")
            logger.error(e)
            break
        
        timestamp = time.time()
        if not addr in received_udp_packets:  # very first time I see the UDP source IP
            logger.info("{0} Client {1} connected".format(datetime.now(), addr))
            with lock:
                received_udp_packets[addr] = ("", 0, 0, 0, time.time())
        with lock:
            (frame, received_frames, expected_fragment_index, expected_frame_index, _) = received_udp_packets[addr]

        # Fetch the header (little endian)
        frame_index = struct.unpack('<H', data[FRAME_INDEX_OFFSET:FRAME_INDEX_OFFSET+FRAME_INDEX_SIZE])[0]
        fragment_index = struct.unpack('<I', data[FRAGMENT_INDEX_OFFSET:FRAGMENT_INDEX_OFFSET+FRAGMENT_INDEX_SIZE])[0]
        #logger.info("Got frame {0}, fragment {1} from {2}".format(frame_index, fragment_index, addr))
        if frame_index != expected_frame_index:
            logger.info("Got frame {0}, fragment {1} from {2}, instead of expected fragment {3}".format(frame_index, fragment_index, addr, expected_fragment_index))
            received_fragments = 0
            expected_frame_index = frame_index
        
        process_frame = False 
        if expected_fragment_index != fragment_index:
            logger.warning("Got fragment {0} instead of expected fragment {1} in the frame {2}".format(
                fragment_index, expected_fragment_index, frame_index))
        if frame_index != expected_frame_index:
            logger.warning("Got frame {0} instead of expected frame {1}".format(
                frame_index, expected_frame_index))
            # This is a new frame
            if len(frame) < expected_frame_size:
                logger.warning("Got {0} bytes instead of expected {1} bytes for the resolution {2}x{3} in frame {4}".format(
                    len(frame), expected_frame_size, width, height, frame_index))
            process_frame = True
            expected_frame_index = frame_index
            expected_fragment_index = 1
        else:
            frame = frame + data[HEADER_SIZE:]
            expected_fragment_index = fragment_index + 1
            
        if len(frame) > expected_frame_size:
            logger.warning("Got {0} bytes instead of expected {1} bytes for the resolution {2}x{3} in frame {4}. Ignore the data".format(
                len(frame), expected_frame_size, width, height, frame_index))
            expected_frame_index = frame_index+1
        elif len(frame) >= expected_frame_size:
            process_frame = True
            expected_frame_index = frame_index+1
            expected_fragment_index = 0

        # The 'frame' contains a whole image - save the data to the rgb565 file
        if process_frame:
            thread.start_new_thread(save_frame_to_file, (filename_base, addr, frame, frame_index, ffmpeg_path))
            received_frames = received_frames + 1
            frame = ""

        # update the dictionary
        with lock:
            if (expected_frame_index >= 64*1024): # handle wrap around of the 2 bytes of the frame index
                expected_frame_index = 0
            received_udp_packets[addr] = (frame, received_frames, expected_fragment_index, expected_frame_index, timestamp)

def run_udp_rx(arguments, simulation=False):
    while True:
        if (not simulation):
            filename_out = arguments["--fileout"]
            (result, fileout) = open_file(filename_out, 'wb')
            if not result:
                logger.error("Failed to open file '{0}' for writing".format(filename_out))
                break

        (result, width, height) = parse_arguments_resolution(arguments["--resolution"])
        if not result:
            break

        udp_port_str = arguments["--port"]
        (result, udp_port) = convert_to_int(udp_port_str, 10)
        if not result:
            logger.error("Failed to parse UDP port number '{0}'".format(udp_port_str))
            break
        
        (result, ffmpeg_path) = parse_arguments_ffmpeg(arguments)

        try:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.bind(("127.0.0.1", udp_port))
        except Exception as e:
            logger.error("Failed to bind UDP port {0}".format(udp_port))
            logger.error(e)
            break

        if (not simulation):
            run_udp_rx_thread(filename_out, udp_socket, width, height, ffmpeg_path)
        else:
            run_udp_rx_simulation(udp_socket, width, height)

        break

def run_udptx(arguments):
    while True:
        filename_in = arguments["--filein"]
        (result, file_in) = open_file(filename_in, 'rb')
        if not result:
            logger.error("Failed to open file '{0}' for writing".format(filename_in))
            break
        
        udp_port_str = arguments["--port"]
        (result, udp_port) = convert_to_int(udp_port_str, 10)
        if not result:
            logger.error("Failed to parse UDP port number '{0}'".format(udp_port_str))
            break

        max_frame_rate_str = arguments["--rate"]
        (result, max_frame_rate) = convert_to_int(max_frame_rate_str, 10)
        if not result:
            logger.error("Failed to parse frame rate '{0}'".format(max_frame_rate_str))
            break
        
        ip_address = arguments["--ip"]
        
        break
        
    if  not result:
        return

    data = file_in.read()
    file_in.close()
    frame_index = 0
    fragment_index = 0
    fragment_size = 1320
    bytes_sent = 0
    fragments_sent = 0
    rate_limiter_frames_sent = 0
    fps = 0
    fps_start = time.time()
    rate_limiter_timestamp = time.time()
    fps_period = 1.0
    
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        packet = ""
        packet = packet + struct.pack("<H", frame_index)
        packet = packet + struct.pack("<I", fragment_index)
        bytes_to_send = fragment_size
        if (fragment_size+bytes_sent) > len(data):
            bytes_to_send = len(data) - bytes_sent
        packet = packet + data[bytes_sent:bytes_sent+bytes_to_send]
        #logger.info("Sending frame {0}, fragment {1}, {2} bytes from {3}".format(frame_index, fragment_index, bytes_sent, len(data)))
        udp_socket.sendto(packet, (ip_address, udp_port))
        
        fragment_index = fragment_index + 1
        bytes_sent = bytes_sent + bytes_to_send
        fragments_sent = fragments_sent + 1
        timestamp = time.time()
        
            
        if bytes_sent >= len(data):
            
            rate_limiter_frames_sent = rate_limiter_frames_sent + 1
            fps = fps + 1
            
            # Calculate difference between the expected transmission time at the given frame rate and actual time 
            delta_time = timestamp - rate_limiter_timestamp
            time_to_sleep = (1.0*rate_limiter_frames_sent/max_frame_rate) - delta_time 
            if (time_to_sleep > 0):
                time.sleep(time_to_sleep)
            if (delta_time > 10):  # Avoid overflow in the counters 
                rate_limiter_timestamp = time.time()
                rate_limiter_frames_sent = 0
            
                
            # print rate
            delta_time = timestamp - fps_start
            if delta_time > fps_period:
                fps_calculated = fps/delta_time
                logger.info("{:3.2f} fps, over {:2.3f}s".format(fps_calculated, delta_time))
                fps = 0
                fps_start = timestamp
                #fps_period = 1.0
                
            frame_index = frame_index + 1
            if (frame_index >= 64*1024): frame_index = 0;
            bytes_sent = 0
            fragment_index = 0
            fragments_sent = 0

if __name__ == '__main__':
    arguments = docopt(__doc__, version='PCAP converter')

    logging.basicConfig()
    logger = logging.getLogger('pcap')
    logger.setLevel(logging.INFO)

    is_convert = arguments["convert"]
    is_udprx = arguments["udprx"]
    is_udprxsim = arguments["udprxsim"]
    is_udptx = arguments["udptx"]

    if is_convert:
        convert_image(arguments)
    elif is_udprx:
        run_udp_rx(arguments)
    elif is_udprxsim:
        run_udp_rx(arguments, True)
    elif is_udptx:
        run_udptx(arguments)
