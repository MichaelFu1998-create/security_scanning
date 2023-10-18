def _convert_fancy(self, field):
        """Convert to a list (sep != None) and convert list elements."""
        if self.sep is False:
            x = self._convert_singlet(field)
        else:
            x = tuple([self._convert_singlet(s) for s in field.split(self.sep)])
            if len(x) == 0:
                x = ''
            elif len(x) == 1:
                x = x[0]
        #print "%r --> %r" % (field, x)
        return x