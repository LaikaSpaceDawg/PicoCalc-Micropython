import uos

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
    return 0

def files():
    entries = uos.listdir()
    
    # Print each entry with its size
    print("")
    for entry in entries:
        try:
            stat = uos.stat(entry)
            size = stat[6]
            if not uos.stat(entry)[0] & 0x4000:
                readable_size = human_readable_size(size)
                print(f"{entry:<28} {readable_size:<9}") 
        except OSError:
            print(f"Error accessing {entry}")

    return 0