def settingshelp(self, width=0):
        """Return a summary of program options, their values and origins.
        
        width is maximum allowed page width, use self.width if 0.
        """
        out = []
        out.append(self._wrap(self.docs['title'], width=width))
        if self.docs['description']:
            out.append(self._wrap(self.docs['description'], indent=2, width=width))
        out.append('')
        out.append('SETTINGS:')
        out.append(self.strsettings(indent=2, width=width))
        out.append('')
        return '\n'.join(out)