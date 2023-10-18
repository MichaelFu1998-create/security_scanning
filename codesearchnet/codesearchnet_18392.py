def optionhelp(self, indent=0, maxindent=25, width=79):
        """Return user friendly help on program options."""
        def makelabels(option):
            labels = '%*s--%s' % (indent, ' ', option.name)
            if option.abbreviation:
                labels += ', -' + option.abbreviation
            return labels + ': '
        docs = []
        helpindent = _autoindent([makelabels(o) for o in self.options.values()], indent, maxindent)
        for name in self.option_order:
            option = self.options[name]
            labels = makelabels(option)
            helpstring = "%s(%s). %s" % (option.formatname, option.strvalue, option.docs)
            wrapped = self._wrap_labelled(labels, helpstring, helpindent, width)
            docs.extend(wrapped)
        return '\n'.join(docs)