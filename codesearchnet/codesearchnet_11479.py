def send_string(self, tosend, ypos=None, xpos=None):
        """
            Send a string to the screen at the current cursor location or at
            screen co-ordinates `ypos`/`xpos` if they are both given.

            Co-ordinates are 1 based, as listed in the status area of the
            terminal.
        """
        if xpos is not None and ypos is not None:
            self.move_to(ypos, xpos)

        # escape double quotes in the data to send
        tosend = tosend.replace('"', '"')

        self.exec_command('String("{0}")'.format(tosend).encode("ascii"))