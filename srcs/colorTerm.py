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


def displayMenu(menuTitle, optionList, color, tabs=0):
    nOpt = "├"
    lastOpt = "└"
    dash = "─"
    i = 1
    tabsLine = ''
    tabsSpace = ''
    if tabs > 0:
        tabsLine = tabs * ' ' + lastOpt + dash
        tabsSpace = (tabs + 2) * ' '
    printc(f"{tabsLine}{menuTitle}", BOLD + color)
    for opt in optionList:
        if i < len(optionList):
            bullet = nOpt
        else:
            bullet = lastOpt
        printc(f"{tabsSpace}{bullet}{dash}{i}{dash} {opt}", color)
        i += 1
    while True:
        x = input("> ")
        if x in optionList:
            return optionList.index(x)
        try:
            xi = int(x) - 1
            if xi >= len(optionList) or xi < 0:
                raise ValueError("out of range")
            return xi
        except ValueError:
            printc("Not a valid input", RED)
