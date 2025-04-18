from picocalc import PicoDisplay, PicoKeyboard
import os
import vt
import sys
from pye import pye_edit
# Mount SD card to /sd on boot
import picocalc_globals
from picocalc_globals import colors

from picocalc_system import run as run
from picocalc_system import files as files
from picocalc_system import memory as memory
from picocalc_system import disk as disk
from picocalc_system import clear as clear

from picocalc_system import initsd as initsd
from picocalc_system import killsd as killsd

pc_display = PicoDisplay(320,320)#display
pc_keyboard = PicoKeyboard()#keyboard
sd = initsd()#sd card
#picocalc_globals.fb=FBConsole(pd, bgcolor=colors.bgdefault, fgcolor=colors.fgdefault, width=320, height=320,readobj=kb,fontX=8,fontY=10)
#os.dupterm(picocalc_globals.fb)
pc_terminal = vt.vt(pc_display,pc_keyboard,sd=sd)#terminal

_usb = sys.stdin

def usb_debug(msg):
    if isinstance(msg, str):
        _usb.write(msg)
    else:
        _usb.write(str(msg))
    _usb.write('\r\n')

def edit(*args, tab_size=2, undo=50):
    ret = pye_edit(args, tab_size=tab_size, undo=undo, io_device=pc_terminal)
    return ret

os.dupterm(pc_terminal) 


#we may move all the init to boot.py later, but for now we want to keep it in main.py for testing purposes