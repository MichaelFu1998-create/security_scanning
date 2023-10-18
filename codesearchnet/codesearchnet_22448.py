def iter_format_block(
            self, text=None,
            width=60, chars=False, fill=False, newlines=False,
            append=None, prepend=None, strip_first=False, strip_last=False,
            lstrip=False):
        """ Iterate over lines in a formatted block of text.
            This iterator allows you to prepend to each line.
            For basic blocks see iter_block().


            Arguments:
                text        : String to format.

                width       : Maximum width for each line. The prepend string
                              is not included in this calculation.
                              Default: 60

                chars       : Whether to wrap on characters instead of spaces.
                              Default: False
                fill        : Insert spaces between words so that each line is
                              the same width. This overrides `chars`.
                              Default: False

                newlines    : Whether to preserve newlines in the original
                              string.
                              Default: False

                append      : String to append after each line.

                prepend     : String to prepend before each line.

                strip_first : Whether to omit the prepend string for the first
                              line.
                              Default: False

                              Example (when using prepend='$'):
                               Without strip_first -> '$this', '$that'
                               With strip_first -> 'this', '$that'

                strip_last  : Whether to omit the append string for the last
                              line (like strip_first does for prepend).
                              Default: False

                lstrip      : Whether to remove leading spaces from each line.
                              This doesn't include any spaces in `prepend`.
                              Default: False
        """
        if fill:
            chars = False

        iterlines = self.iter_block(
            (self.text if text is None else text) or '',
            width=width,
            chars=chars,
            newlines=newlines,
            lstrip=lstrip,
        )

        if not (prepend or append):
            # Shortcut some of the logic below when not prepending/appending.
            if fill:
                yield from (
                    self.expand_words(l, width=width) for l in iterlines
                )
            else:
                yield from iterlines
        else:
            # Prepend, append, or both prepend/append to each line.
            if prepend:
                prependlen = len(prepend)
            else:
                # No prepend, stripping not necessary and shouldn't be tried.
                strip_first = False
                prependlen = 0
            if append:
                # Unfortunately appending mean exhausting the generator.
                # I don't know where the last line is if I don't.
                lines = list(iterlines)
                lasti = len(lines) - 1
                iterlines = (l for l in lines)
                appendlen = len(append)
            else:
                # No append, stripping not necessary and shouldn't be tried.
                strip_last = False
                appendlen = 0
                lasti = -1
            for i, l in enumerate(self.iter_add_text(
                    iterlines,
                    prepend=prepend,
                    append=append)):
                if strip_first and (i == 0):
                    # Strip the prepend that iter_add_text() added.
                    l = l[prependlen:]
                elif strip_last and (i == lasti):
                    # Strip the append that iter_add_text() added.
                    l = l[:-appendlen]
                if fill:
                    yield self.expand_words(l, width=width)
                else:
                    yield l