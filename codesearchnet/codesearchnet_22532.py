def _wrap_color(self, code, text, format=None, style=None):
        """ Colors text with code and given format """
        color = None
        if code[:3] == self.bg.PREFIX:
            color = self.bg.COLORS.get(code, None)
        if not color:
            color = self.fg.COLORS.get(code, None)

        if not color:
            raise Exception('Color code not found')

        if format and format not in self.formats:
            raise Exception('Color format not found')

        fmt = "0;"
        if format == 'bold':
            fmt = "1;"
        elif format == 'underline':
            fmt = "4;"

        # Manage the format
        parts = color.split('[')
        color = '{0}[{1}{2}'.format(parts[0], fmt, parts[1])

        if self.has_colors and self.colors_enabled:
            # Set brightness
            st = ''
            if style:
                st = self.st.COLORS.get(style, '')
            return "{0}{1}{2}{3}".format(st, color, text, self.st.COLORS['reset_all'])
        else:
            return text