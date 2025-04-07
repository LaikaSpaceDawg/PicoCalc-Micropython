from picocalc import PicoDisplay, PicoKeyboard
from fbconsole import FBConsole
import os

colors = {
    "BLACK": 0,
    "RED": 1,
    "GREEN": 2,
    "YELLOW": 3,
    "BLUE": 4,
    "PURPLE": 5,
    "CYAN": 6,
    "WHITE": 7,
    "GREY": 8,
    "BRRED": 9,
    "BRGREEN": 10,
    "BRYELLOW": 11,
    "BRBLUE": 12,
    "BRPURPLE": 13,
    "BRCYAN": 14,
    "BRWHITE": 15
}

from picocalc_system import run as run
from picocalc_system import files as files
        
pd = PicoDisplay(320,320)
kb = PicoKeyboard()
fb=FBConsole( pd, bgcolor=colors["BLACK"], fgcolor=colors["WHITE"], width=320, height=320,readobj=kb,fontX=8,fontY=10)
os.dupterm(fb)