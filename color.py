import colorama

colorama.init()

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
NORMAL = "\x1b[0m"

def colorize(text, color = WHITE):
    """Return colorized string"""
    return "\x1b[1;{0}m".format(str(30 + color)) + text + "\x1b[1;{0}m".format(str(30 + WHITE))
