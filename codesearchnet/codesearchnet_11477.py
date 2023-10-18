def wait_for_field(self):
        """
            Wait until the screen is ready, the cursor has been positioned
            on a modifiable field, and the keyboard is unlocked.

            Sometimes the server will "unlock" the keyboard but the screen will
            not yet be ready.  In that case, an attempt to read or write to the
            screen will result in a 'E' keyboard status because we tried to
            read from a screen that is not yet ready.

            Using this method tells the client to wait until a field is
            detected and the cursor has been positioned on it.
        """
        self.exec_command("Wait({0}, InputField)".format(self.timeout).encode("ascii"))
        if self.status.keyboard != b"U":
            raise KeyboardStateError(
                "keyboard not unlocked, state was: {0}".format(
                    self.status.keyboard.decode("ascii")
                )
            )