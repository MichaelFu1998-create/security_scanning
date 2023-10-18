def fill_field(self, ypos, xpos, tosend, length):
        """
            clears the field at the position given and inserts the string
            `tosend`

            tosend: the string to insert
            length: the length of the field

            Co-ordinates are 1 based, as listed in the status area of the
            terminal.

            raises: FieldTruncateError if `tosend` is longer than
                `length`.
        """
        if length < len(tosend):
            raise FieldTruncateError('length limit %d, but got "%s"' % (length, tosend))
        if xpos is not None and ypos is not None:
            self.move_to(ypos, xpos)
        self.delete_field()
        self.send_string(tosend)