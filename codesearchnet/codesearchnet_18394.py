def format_usage(self, usage=None):
        """Return a formatted usage string. 
        
        If usage is None, use self.docs['usage'], and if that is also None, 
        generate one.
        """
        if usage is None:
            usage = self.docs['usage']
        if usage is not None:
            return usage[0] % self.docvars
        usage = self.docvars['command']
        if self.basic_option_names.get('help'):
            usage += ' [--%s]' % self.basic_option_names.get('help')
        if self.options:
            usage += ' <OPTIONS>'
        optional = 0
        for posarg in self.positional_args:
            usage += ' '
            if posarg.optional:
                usage += "[" 
                optional += 1
            usage += posarg.displayname
            if posarg.recurring:
                usage += ' [%s2 [...]]' % posarg.displayname
        usage += ']' * optional
        return usage