def _build_arg_list(self, **kwargs):
        """Build list of arguments from the dict; keys must be valid  gromacs flags."""
        arglist = []
        for flag, value in kwargs.items():
            # XXX: check flag against allowed values
            flag = str(flag)
            if flag.startswith('_'):
                flag = flag[1:]                 # python-illegal keywords are '_'-quoted
            if not flag.startswith('-'):
                flag = '-' + flag               # now flag is guaranteed to start with '-'
            if value is True:
                arglist.append(flag)            # simple command line flag
            elif value is False:
                if flag.startswith('-no'):
                    # negate a negated flag ('noX=False' --> X=True --> -X ... but who uses that?)
                    arglist.append('-' + flag[3:])
                else:
                    arglist.append('-no' + flag[1:])  # gromacs switches booleans by prefixing 'no'
            elif value is None:
                pass                            # ignore flag = None
            else:
                try:
                    arglist.extend([flag] + value) # option with value list
                except TypeError:
                    arglist.extend([flag, value])  # option with single value
        return list(map(str, arglist))