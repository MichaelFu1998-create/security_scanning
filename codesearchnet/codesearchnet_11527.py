def input(self, input, song):
        """Input callback, handles key presses
        """
        try:
            cmd = getattr(self, self.CMD_MAP[input][1])
        except (IndexError, KeyError):
            return self.screen.print_error(
                "Invalid command {!r}!".format(input))

        cmd(song)