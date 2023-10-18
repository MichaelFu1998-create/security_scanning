def posarghelp(self, indent=0, maxindent=25, width=79):
        """Return user friendly help on positional arguments in the program."""
        docs = []
        makelabel = lambda posarg: ' ' * indent + posarg.displayname + ': '
        helpindent = _autoindent([makelabel(p) for p in self.positional_args], indent, maxindent)
        for posarg in self.positional_args:
            label = makelabel(posarg)
            text = posarg.formatname + '. ' + posarg.docs
            wrapped = self._wrap_labelled(label, text, helpindent, width)
            docs.extend(wrapped)
        return '\n'.join(docs)