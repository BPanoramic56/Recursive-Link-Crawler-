class TerminalColor(object):
    """
        Creates and stores a random RGB color
    """
    def __init__(self, r, g, b):
        self.red    = r
        self.green  = g
        self.blue   = b

    def getColor(self):
        return f"\033[38;2;{self.red};{self.green};{self.blue}m"

    def getDefaultColor(self):
        return f"\033[0m"
