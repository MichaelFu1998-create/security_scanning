def move_to(self, ypos, xpos):
        """
            move the cursor to the given co-ordinates.  Co-ordinates are 1
            based, as listed in the status area of the terminal.
        """
        # the screen's co-ordinates are 1 based, but the command is 0 based
        xpos -= 1
        ypos -= 1
        self.exec_command("MoveCursor({0}, {1})".format(ypos, xpos).encode("ascii"))