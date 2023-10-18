def iter_add_text(self, lines, prepend=None, append=None):
        """ Prepend or append text to lines. Yields each line. """
        if (prepend is None) and (append is None):
            yield from lines
        else:
            # Build up a format string, with optional {prepend}/{append}
            fmtpcs = ['{prepend}'] if prepend else []
            fmtpcs.append('{line}')
            if append:
                fmtpcs.append('{append}')
            fmtstr = ''.join(fmtpcs)
            yield from (
                fmtstr.format(prepend=prepend, line=line, append=append)
                for line in lines
            )