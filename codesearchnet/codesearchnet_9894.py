def advance_past_string_with_gdb_escapes(self, chars_to_remove_gdb_escape=None):
        """characters that gdb escapes that should not be
        escaped by this parser
        """

        if chars_to_remove_gdb_escape is None:
            chars_to_remove_gdb_escape = ['"']

        buf = ""
        while True:
            c = self.raw_text[self.index]
            self.index += 1
            logging.debug("%s", fmt_cyan(c))

            if c == "\\":
                # We are on a backslash and there is another character after the backslash
                # to parse. Handle this case specially since gdb escaped it for us

                # Get the next char that is being escaped
                c2 = self.raw_text[self.index]
                self.index += 1
                # only store the escaped character in the buffer; don't store the backslash
                # (don't leave it escaped)
                buf += c2

            elif c == '"':
                # Quote is closed. Exit (and don't include the end quote).
                break

            else:
                # capture this character, and keep capturing
                buf += c
        return buf