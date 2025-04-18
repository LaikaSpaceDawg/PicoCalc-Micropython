class Colors:
    # Define class attributes for each color
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    PURPLE = 5
    CYAN = 6
    WHITE = 7
    GREY = 8
    BRRED = 9
    BRGREEN = 10
    BRYELLOW = 11
    BRBLUE = 12
    BRPURPLE = 13
    BRCYAN = 14
    BRWHITE = 15
    
    ERROR = BRRED
    SUCCESS = GREEN
    WARNING = BRYELLOW
    
    def __init__(self, bgdefault=None, fgdefault=None):
        self.bgdefault = bgdefault if bgdefault is not None else self.BLACK
        self.fgdefault = fgdefault if fgdefault is not None else self.WHITE

    def set_bgdefault(self, color):
        self.bgdefault = color

    def set_fgdefault(self, color):
        self.fgdefault = color
        
fb = None
sd = None
colors = Colors()
