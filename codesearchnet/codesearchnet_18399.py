def strsettings(self, indent=0, maxindent=25, width=0):
        """Return user friendly help on positional arguments.        

        indent is the number of spaces preceeding the text on each line. 
        
        The indent of the documentation is dependent on the length of the 
        longest label that is shorter than maxindent. A label longer than 
        maxindent will be printed on its own line.
        
        width is maximum allowed page width, use self.width if 0.
        """
        out = []
        makelabel = lambda name: ' ' * indent + name + ': '
        settingsindent = _autoindent([makelabel(s) for s in self.options], indent, maxindent)
        for name in self.option_order:
            option = self.options[name]
            label = makelabel(name)
            settingshelp = "%s(%s): %s" % (option.formatname, option.strvalue, option.location)
            wrapped = self._wrap_labelled(label, settingshelp, settingsindent, width)
            out.extend(wrapped)
        return '\n'.join(out)