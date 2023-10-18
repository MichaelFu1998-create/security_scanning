def _wrap(self, text, indent=0, width=0):
        """Textwrap an indented paragraph.
        ARGS:
        width = 0 <int>:
            Maximum allowed page width. 0 means use default from
            self.iMaxHelpWidth.

        """
        text = _list(text)
        if not width:
            width = self.width
        paragraph = text[0].lstrip()
        s = ' ' * (len(text[0]) - len(paragraph) + indent)
        wrapped = textwrap.wrap(paragraph.strip(), width, initial_indent=s, subsequent_indent=s)
        return '\n'.join(wrapped)