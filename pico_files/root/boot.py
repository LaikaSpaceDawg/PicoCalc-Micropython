from machine import freq
from picocalc import PicoDisplay, PicoKeyboard
import vt
from pye import pye_edit
from colorer import Fore, Back, Style, print, autoreset

# Initialize colorer
autoreset(True)

# Constants
terminal_rows = 40
terminal_width = 53
non_scrolling_lines = 2
multithreading = True
eigenmath_en = True
show_bar = True

# Set CPU Frequency
try:
    machine.freq(200000000)
except:
    pass

# Terminal Initialization
def initialize_terminal():
    global non_scrolling_lines, terminal_rows
    print(f"\033[{non_scrolling_lines + 1};{terminal_rows}r", end='')

# Main Program Execution
try:
    if show_bar:
        # Determine MicroPython version
        from sys import version
        index = version.find('MicroPython v')
        if index != -1:
            MICROPYTHON_VERSION = version[index + 13:].split('-')[0]
        initialize_terminal()

    if eigenmath_en:
        from eigenmath import EigenMath
        em = EigenMath(300 * 1024)

    pc_display = PicoDisplay(320, 320, multithreading)
    
    displayflush = True
    def upd(timer=None):
        global displayflush
        displayflush = True

    # Multithreading setup
    if multithreading:
        from machine import lightsleep
        import picocalcdisplay
        import _thread, asyncio
        threadlock = _thread.allocate_lock()
        asynclock = asyncio.Lock()
        
        lightsleep(50)
        async def flushthread():
            global displayflush
            while True:
                if displayflush:
                    displayflush = False
                    async with asynclock:
                        with threadlock:
                            picocalcdisplay.update(0)
                await asyncio.sleep_ms(5)

        async def core1():
            asyncio.create_task(flushthread())
            # asyncio.create_task(powersaver())
            while True:
                await asyncio.sleep(1)

        def thread1():
            asyncio.run(core1())

        _thread.start_new_thread(thread1, ())

    pc_keyboard = PicoKeyboard()
    pc_terminal = vt.vt(pc_display, pc_keyboard)
    
    from picocalc import display, keyboard, terminal
    display = pc_display
    keyboard = pc_keyboard
    terminal = pc_terminal
    
    from os import dupterm
    dupterm(pc_terminal)
    print("\n")

    if multithreading:
        from machine import Timer
        tupd = machine.Timer()
        tupd.init(mode=machine.Timer.PERIODIC, period=25, callback=upd)

    # Header handling
    from picocalc import editing
    def print_header():
        if not editing:
            global MICROPYTHON_VERSION
            description = f"PicoCalc MicroPython (ver {MICROPYTHON_VERSION})"
            battery = keyboard.battery()
            current_time = pc_rtc.time()
            left_text = f"Battery: {battery}%"
            right_text = f"{current_time}"
            padding_left_line1 = ' ' * ((terminal_width - len(description)) // 2)
            padding_right_line1 = ' ' * (terminal_width - len(padding_left_line1) - len(description))
            line1 = f"{Style.FLASHING}{padding_left_line1}{description}{padding_right_line1}"
            # Flashing isn't supported, highlights nicely though
            padding_between_left_right_line2 = ' ' * (terminal_width - len(left_text) - len(right_text))
            line2 = f"{Style.FLASHING}{left_text}{padding_between_left_right_line2}{right_text}"
            print("\0337", end='')  # Save cursor and attributes
            print(f"\033[1;1H{line1}", end='')   # Header line 1
            print(f"\033[2;1H{line2}", end='')   # Header line 2
            # Restore cursor position
            print("\0338", end='')

    def update_header(timer=None):
        print_header()
    
    from picocalc import PicoSD, PicoSpeaker, PicoWiFi, PicoRTC
    try:
        pc_rtc = PicoRTC()
        pc_rtc.sync()
    except:
        pass

    if show_bar:
        if not multithreading:
            from machine import Timer
        print_header()
        header_timer = machine.Timer()
        header_timer.init(mode=machine.Timer.PERIODIC, period=5000, callback=update_header)

    # Initialize WiFi
    pc_wifi = PicoWiFi()
    # pc_wifi.aconnect(True)
    pcs_L = PicoSpeaker(26)
    pcs_R = PicoSpeaker(27)

    # Mount SD card
    pc_sd = PicoSD()
    pc_terminal.setsd(pc_sd)
    print(f"{Fore.GREEN}Current Time and Date: {pc_rtc.time()}")
    
    def edit(*args, tab_size=4, undo=50):
        # Dry the key buffer before editing
        pc_terminal.dryBuffer()
        picocalc.editing = True
        return pye_edit(args, tab_size=tab_size, undo=undo, io_device=pc_terminal)
    from picocalc import editor
    editor = edit
    
    # Optional system imports
    try:
        from picocalc_sys import clear, files, memory, disk, run
    except Exception as e:
        print(f"Failed to import sys: {e}")
    
    from sys import stdout
    _usb = stdout
    def usb_debug(msg):
        if isinstance(msg, str):
            _usb.write(msg)
        else:
            _usb.write(str(msg))
        _usb.write('\r\n')
    from picocalc import usb_debug
    usb_debug = usb_debug
    # usb_debug("boot.py done.")
    
except Exception as e:
    import sys
    sys.print_exception(e)
    try:
        os.dupterm(None).write(b"[boot.py error]\n")
    except:
        pass