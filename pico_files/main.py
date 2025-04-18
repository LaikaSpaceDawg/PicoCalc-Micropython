from picocalc import PicoDisplay, PicoKeyboard
from fbconsole import FBConsole
import os

import picocalc_globals
from picocalc_globals import colors

# Change the as [alias] if you want them to use a different command in the REPL
from picocalc_system import run as run
from picocalc_system import files as files
from picocalc_system import memory as memory
from picocalc_system import disk as disk
from picocalc_system import clear as clear

from picocalc_system import initsd as initsd
from picocalc_system import killsd as killsd

# Change these if you want different colors
# colors.set_bgdefault(colors.BLACK)
# colors.set_fgdefault(colors.WHITE)

pd = PicoDisplay(320,320)
kb = PicoKeyboard()
picocalc_globals.fb=FBConsole(pd, bgcolor=colors.bgdefault, fgcolor=colors.fgdefault, width=320, height=320,readobj=kb,fontX=8,fontY=10)
os.dupterm(picocalc_globals.fb)

initsd()