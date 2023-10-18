def iter_block(
            self, text=None,
            width=60, chars=False, newlines=False, lstrip=False):
        """ Iterator that turns a long string into lines no greater than
            'width' in length.
            It can wrap on spaces or characters. It only does basic blocks.
            For prepending see `iter_format_block()`.

            Arguments:
                text     : String to format.
                width    : Maximum width for each line.
                           Default: 60
                chars    : Wrap on characters if true, otherwise on spaces.
                           Default: False
                newlines : Preserve newlines when True.
                           Default: False
                lstrip   : Whether to remove leading spaces from each line.
                           Default: False
        """
        text = (self.text if text is None else text) or ''
        if width < 1:
            width = 1
        fmtline = str.lstrip if lstrip else str

        if chars and (not newlines):
            # Simple block by chars, newlines are treated as a space.
            yield from self.iter_char_block(
                text,
                width=width,
                fmtfunc=fmtline
            )
        elif newlines:
            # Preserve newlines
            for line in text.split('\n'):
                yield from self.iter_block(
                    line,
                    width=width,
                    chars=chars,
                    lstrip=lstrip,
                    newlines=False,
                )
        else:
            # Wrap on spaces (ignores newlines)..
            yield from self.iter_space_block(
                text,
                width=width,
                fmtfunc=fmtline,
            )