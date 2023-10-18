def do_menu(self, line):
        """Display a menu of command-line options. Command syntax is: menu"""
        print('\ta\t\tAnalog measurement.\tEnter index and value as arguments.')
        print('\ta2\t\tAnalog 2 for MMDC.Vol (index 4).')
        print('\tb\t\tBinary measurement.\tEnter index and value as arguments.')
        print('\tb0\t\tBinary False for MMDC1.Amp.range (index 6).')
        print('\tc\t\tCounter measurement.\tEnter index and value as arguments.')
        print('\td\t\tDoubleBit DETERMINED_ON.\tEnter index as an argument.')
        print('\thelp\t\tDisplay command-line help.')
        print('\tmenu\t\tDisplay this menu.')
        print('\tquit')