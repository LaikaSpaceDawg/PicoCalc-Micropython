import uos
import machine
import sdcard

def human_readable_size(size):
    # Define size units
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"  # Format size with 2 decimal places
        size /= 1024
    return f"{size:.2f} PB"  # Fallback to PB for extremely large files

def run(filename):
    try:
        exec(open(filename).read())
    except OSError:
        print(f"Failed to open file: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return

def files(directory="/"):
    try:
        # List entries in the specified directory
        entries = uos.listdir(directory)
    except OSError as e:
        print(f"Error accessing directory {directory}: {e}")
        return

    print(f"\nContents of directory: {directory}\n")
    for entry in entries:
        try:
            # Construct the full path
            full_path = directory.rstrip("/") + "/" + entry
            stat = uos.stat(full_path)
            size = stat[6]

            # Check if entry is a directory or a file
            if stat[0] & 0x4000:  # Directory
                print(f"{entry:<25} <DIR>")
            else:  # File
                readable_size = human_readable_size(size)
                print(f"{entry:<25} {readable_size:<9}")
        except OSError as e:
            print(f"Error accessing {entry}: {e}")
    return

def initsd():
    try:
        sd = sdcard.SDCard(
            machine.SPI(0,
                      baudrate=1000000,
                      polarity=0,
                      phase=0,
                      sck=18,
                      mosi=19,
                      miso=16), machine.Pin(17))
        # Mount filesystem
        uos.mount(sd, "/sd")
    except Exception as e:
        print("Failed to mount SD card:", e)
    return sd

def killsd(sd="/sd"):
    # DOESNT WORK
    try:
        uos.umount(sd)
    except Exception as e: 
        print("Failed to unmount SD card:", e)
    return