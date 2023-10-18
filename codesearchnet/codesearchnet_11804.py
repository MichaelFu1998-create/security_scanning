def vprint(self, *args, **kwargs):
        """
        When verbose is set, acts like the normal print() function.
        Otherwise, does nothing.
        """
        if self.verbose:
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)
            caller_name = calframe[1][3]
            prefix = '%s.%s:' % (self.name.lower(), caller_name)
            print(prefix, *args, **kwargs)