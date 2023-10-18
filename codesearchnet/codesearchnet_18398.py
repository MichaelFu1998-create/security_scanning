def shorthelp(self, width=0):
        """Return brief help containing Title and usage instructions.
        ARGS:
        width = 0 <int>:
            Maximum allowed page width. 0 means use default from
            self.iMaxHelpWidth.

        """
        out = []
        out.append(self._wrap(self.docs['title'], width=width))
        if self.docs['description']:
            out.append(self._wrap(self.docs['description'], indent=2, width=width))
        out.append('')
        out.append(self._wrapusage(width=width))
        out.append('')
        return '\n'.join(out)