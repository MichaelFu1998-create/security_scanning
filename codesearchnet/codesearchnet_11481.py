def string_found(self, ypos, xpos, string):
        """
            Return True if `string` is found at screen co-ordinates
            `ypos`/`xpos`, False otherwise.

            Co-ordinates are 1 based, as listed in the status area of the
            terminal.
        """
        found = self.string_get(ypos, xpos, len(string))
        log.debug('string_found() saw "{0}"'.format(found))
        return found == string