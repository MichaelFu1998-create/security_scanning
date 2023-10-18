def format(
            self, text=None,
            width=60, chars=False, fill=False, newlines=False,
            prepend=None, append=None, strip_first=False, strip_last=False,
            lstrip=False):
        """ Format a long string into a block of newline seperated text.
            Arguments:
                See iter_format_block().
        """
        # Basic usage of iter_format_block(), for convenience.
        return '\n'.join(
            self.iter_format_block(
                (self.text if text is None else text) or '',
                prepend=prepend,
                append=append,
                strip_first=strip_first,
                strip_last=strip_last,
                width=width,
                chars=chars,
                fill=fill,
                newlines=newlines,
                lstrip=lstrip
            )
        )