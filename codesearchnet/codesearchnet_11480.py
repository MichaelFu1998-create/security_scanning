def string_get(self, ypos, xpos, length):
        """
            Get a string of `length` at screen co-ordinates `ypos`/`xpos`

            Co-ordinates are 1 based, as listed in the status area of the
            terminal.
        """
        # the screen's co-ordinates are 1 based, but the command is 0 based
        xpos -= 1
        ypos -= 1
        cmd = self.exec_command(
            "Ascii({0},{1},{2})".format(ypos, xpos, length).encode("ascii")
        )
        # this usage of ascii should only return a single line of data
        assert len(cmd.data) == 1, cmd.data
        return cmd.data[0].decode("ascii")