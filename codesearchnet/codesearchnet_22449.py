def iter_space_block(self, text=None, width=60, fmtfunc=str):
        """ Format block by wrapping on spaces. """
        if width < 1:
            width = 1
        curline = ''
        text = (self.text if text is None else text) or ''
        for word in text.split():
            possibleline = ' '.join((curline, word)) if curline else word
            # Ignore escape codes.
            codelen = sum(len(s) for s in get_codes(possibleline))
            reallen = len(possibleline) - codelen
            if reallen > width:
                # This word would exceed the limit, start a new line with
                # it.
                yield fmtfunc(curline)
                curline = word
            else:
                curline = possibleline
        # yield the last line.
        if curline:
            yield fmtfunc(curline)