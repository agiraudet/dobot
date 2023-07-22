RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"


def printc(text, color):
    print(color + text + RESET)


def announce(text, color, who):
    print(f"{BOLD}{color}[{who}]{RESET} {text}")
