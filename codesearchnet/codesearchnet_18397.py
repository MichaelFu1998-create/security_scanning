def _wrapusage(self, usage=None, width=0):
        """Textwrap usage instructions.
        ARGS:
        width = 0 <int>:
            Maximum allowed page width. 0 means use default from
            self.iMaxHelpWidth.

        """
        if not width:
            width = self.width
        return textwrap.fill('USAGE: ' + self.format_usage(usage), width=width, subsequent_indent='    ...')