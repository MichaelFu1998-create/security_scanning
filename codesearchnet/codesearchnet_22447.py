def iter_char_block(self, text=None, width=60, fmtfunc=str):
        """ Format block by splitting on individual characters. """
        if width < 1:
            width = 1
        text = (self.text if text is None else text) or ''
        text = ' '.join(text.split('\n'))
        escapecodes = get_codes(text)
        if not escapecodes:
            # No escape codes, use simple method.
            yield from (
                fmtfunc(text[i:i + width])
                for i in range(0, len(text), width)
            )
        else:
            # Ignore escape codes when counting.
            blockwidth = 0
            block = []
            for i, s in enumerate(get_indices_list(text)):
                block.append(s)
                if len(s) == 1:
                    # Normal char.
                    blockwidth += 1
                if blockwidth == width:
                    yield ''.join(block)
                    block = []
                    blockwidth = 0
            if block:
                yield ''.join(block)