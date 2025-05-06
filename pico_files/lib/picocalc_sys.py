"""
PicoCalc system functions for micropython
Written by: Laika, 4/9/2025

Requires sdcard.py from the official Micropython repository
https://github.com/micropython/micropython-lib/blob/master/micropython/drivers/storage/sdcard/sdcard.py

Features various system functions such as mounting and unmounting the PicoCalc's SD card, a nicer run utility, and an ls utility

"""
import os
import uos
import machine
import sdcard
import gc

import errno

import uasyncio as asyncio
from micropython import const

import urequests

def human_readable_size(size):
    """
    Returns input size in bytes in a human-readable format

    Inputs: size in bytes
    Outputs: size in closest human-readable unit
    """
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    # Fallthrough isnt even possible to be needed on the PicoCalc, neither is TB, but its a universal function
    return f"{size:.2f} PB"

def prepare_for_launch(keep_vars=( "gc", "__name__")):
    for k in list(globals()):
        if k not in keep_vars:
            del globals()[k]
    gc.collect()

def is_dir(path):
    """
    Helper function to shittily replace os.path.exists (not in micropython)
    Absolutely not a good replacement, but decent enough for seeing if the SD is mounted

    Inputs: path to check for
    Outputs: boolean if path is found
    """
    # List the root directory to check for the existence of the desired path
    try:
        directories = os.listdir('/')
        return path.lstrip('/') in directories
    except OSError:
        return False

def clear(lines=None):
    if lines:
        # +2 as a constant correction, might only need to be +1 when used in scripts
        for line in range(lines+2):
            print("\033[1A\033[2K",end='')
    else:
        print("\x1b[2J\x1b[3;1H", end='')

def run(filename):
    """
    Simple run utility.
    Attempts to run python file provided by filename, returns when done.

    Inputs: python file filename/filepath
    Outputs: None, runs file
    """
    try:
        exec(open(filename).read(), globals())
    except OSError:
        print(f"Failed to open file: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return

def files(directory="/"):
    """
    Enhanced ls port.
    Inputs: directory/filepath to list files and directories in
    Outputs: Prints all directories (first) and files (second) in alphabetical order.
    """
    try:
        # List entries in the specified directory
        entries = uos.listdir(directory)
    except OSError as e:
        if e.args[0] == errno.ENOENT:
            print(f"{Fore.RED}Directory {directory} not found.")
        else:
            print(f"{FORE.RED}Error Accessing Directory {directory}: {e}")
        return
    
    print(f"Contents of Directory: {directory}")
    
    # Separate directories and files
    directories = []
    files = []
    
    for entry in entries:
        try:
            full_path = directory.rstrip("/") + "/" + entry
            stat = uos.stat(full_path)
            
            # Check if entry is a directory
            if stat[0] & 0x4000:  # Directory
                directories.append(entry)
            else:  # File
                files.append((entry, stat[6]))
        except OSError as e:
            print(f"{Fore.RED}Error accessing {entry}: {e}")

    # Sort directories and files
    directories.sort()
    files.sort(key=lambda x: x[0])
    
    # Display directories
    for dir_name in directories:
        print(f"{dir_name:<25} <DIR>")
    
    # Display files
    for file_name, size in files:
        readable_size = human_readable_size(size)
        print(f"{file_name:<25} {readable_size:<9}")

    return

def memory():
    """
    Prints available and free RAM

    Inputs: None
    Outputs: None, prints RAM status
    """
    gc.collect()
    # Get the available and free RAM
    free_memory = gc.mem_free()
    allocated_memory = gc.mem_alloc()

    # Total memory is the sum of free and allocated memory
    total_memory = free_memory + allocated_memory

    human_readable_total = human_readable_size(total_memory)
    human_readable_free = human_readable_size(free_memory)

    print(f"Total RAM: {human_readable_total}")
    print(f"Free RAM: {human_readable_free}")

def disk():
    """
    Prints available flash and SD card space (if mounted) as well as totals

    Input: None
    Outputs: None, prints disk statuses
    """
    filesystem_paths = ['/', '/sd']
    for path in filesystem_paths:
        if is_dir(path) or path == '/':
            if path == '/sd':
                # Indicate SD card status
                print("SD card mounted.")
                print(f"{Fore.YELLOW}Indexing SD Card, Please Wait.")
            try:
                fs_stat = os.statvfs(path)
                block_size = fs_stat[1]
                total_blocks = fs_stat[2]
                free_blocks = fs_stat[3]
                total_size = total_blocks * block_size
                free_size = free_blocks * block_size
                human_readable_total = human_readable_size(total_size)
                human_readable_free = human_readable_size(free_size)

                if path == '/':
                    print(f"Total filesystem size: {human_readable_total}")
                    print(f"Free filesystem space: {human_readable_free}")
                else:
                    print(f"Total SD size: {human_readable_total}")
                    print(f"Free SD space: {human_readable_free}")

            except OSError:
                print(f"{Fore.RED}Unexpected error accessing filesystem at '{path}'.")

        else:
            if path == '/sd':
                print("No SD Card Mounted.")

#provided by _burr_
def screenshot_bmp(buffer, filename, width=320, height=320, palette=None):
    FILE_HEADER_SIZE = const(14)
    INFO_HEADER_SIZE = const(40)
    PALETTE_SIZE = const(16 * 4)  # 16 colors × 4 bytes (BGRA)

    # Default VT100 16-color palette
    if palette is None:
        lut = picocalc.display.getLUT() #get memoryview of the current LUT
        palette = []
        for i in range(16):
            raw = lut[i]
            raw = ((raw & 0xFF) << 8) | (raw >> 8)

            r = ((raw >> 11) & 0x1F) << 3
            g = ((raw >> 5) & 0x3F) << 2
            b = (raw & 0x1F) << 3
            palette.append((r, g, b))
        '''
        palette = [
            (0x00, 0x00, 0x00),  # 0 black
            (0x80, 0x00, 0x00),  # 1 red
            (0x00, 0x80, 0x00),  # 2 green
            (0x80, 0x80, 0x00),  # 3 yellow
            (0x00, 0x00, 0x80),  # 4 blue
            (0x80, 0x00, 0x80),  # 5 magenta
            (0x00, 0x80, 0x80),  # 6 cyan
            (0xc0, 0xc0, 0xc0),  # 7 white (light gray)
            (0x80, 0x80, 0x80),  # 8 bright black (dark gray)
            (0xff, 0x00, 0x00),  # 9 bright red
            (0x00, 0xff, 0x00),  # 10 bright green
            (0xff, 0xff, 0x00),  # 11 bright yellow
            (0x00, 0x00, 0xff),  # 12 bright blue
            (0xff, 0x00, 0xff),  # 13 bright magenta
            (0x00, 0xff, 0xff),  # 14 bright cyan
            (0xff, 0xff, 0xff),  # 15 bright white
        ]
        '''
    row_bytes = ((width + 1) // 2 + 3) & ~3  # align to 4-byte boundary
    pixel_data_size = row_bytes * height
    file_size = FILE_HEADER_SIZE + INFO_HEADER_SIZE + PALETTE_SIZE + pixel_data_size
    pixel_data_offset = FILE_HEADER_SIZE + INFO_HEADER_SIZE + PALETTE_SIZE

    with open(filename, "wb") as f:
        # BMP file header
        f.write(b'BM')
        f.write(file_size.to_bytes(4, 'little'))
        f.write((0).to_bytes(4, 'little'))  # Reserved
        f.write(pixel_data_offset.to_bytes(4, 'little'))

        # DIB header
        f.write(INFO_HEADER_SIZE.to_bytes(4, 'little'))
        f.write(width.to_bytes(4, 'little'))
        f.write(height.to_bytes(4, 'little'))
        f.write((1).to_bytes(2, 'little'))  # Planes
        f.write((4).to_bytes(2, 'little'))  # Bits per pixel
        f.write((0).to_bytes(4, 'little'))  # No compression
        f.write(pixel_data_size.to_bytes(4, 'little'))
        f.write((0).to_bytes(4, 'little'))  # X pixels per meter
        f.write((0).to_bytes(4, 'little'))  # Y pixels per meter
        f.write((16).to_bytes(4, 'little'))  # Colors in palette
        f.write((0).to_bytes(4, 'little'))  # Important colors

        # Palette (BGRA)
        for r, g, b in palette:
            f.write(bytes([b, g, r, 0]))

        # Pixel data (bottom-up)
        for row in range(height - 1, -1, -1):
            start = row * ((width + 1) // 2)
            row_data = buffer[start:start + ((width + 1) // 2)]
            f.write(row_data)
            f.write(bytes(row_bytes - len(row_data)))  # Padding

def read_config(file_path):
    try:
        with open(file_path, 'r') as file:
            line = file.readline().strip()
            # Remove the quotes and split by commas
            config = [item.strip('"') for item in line.split(',')]
            if len(config) == 3:
                return config
            else:
                raise ValueError("Invalid config file format.")
        exec(open(filename).read(), globals())
    except OSError:
        print(f"Failed to open file: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return

# Upload function using WebDAV
def www_upload(file_name_to_upload):
    config = read_config("/www_conf.txt")
    if not config:
        print("Could not read config. Exiting.")
        return

    webdav_url, username, password = config

    try:
        with open(file_name_to_upload, 'rb') as file:
            file_content = file.read()

        headers = {'Content-Type': 'application/octet-stream'}
        response = urequests.put(webdav_url + '/' + file_name_to_upload.split("/")[-1],
                                 headers=headers,
                                 data=file_content,
                                 auth=(username, password))
        print('Upload response:', response.status_code, response.content)
        response.close()
    except OSError as e:
        print('Failed to read file:', e)
    except Exception as e:
        print('Error:', e)
        
def scan():
    i2c = machine.I2C(1, sda=machine.Pin(6), scl=machine.Pin(7), freq=10000)
    print('Scan I2C bus...')
    devices = i2c.scan()
    if len(devices) == 0:
      print("No Devices Found!")
    else:
      print('Devices Found:',len(devices))

      for device in devices:
        print(f"Decimal: {device:3} | Hex: {hex(device)}")
