def transform_args(self, *args, **kwargs):
        """Transform arguments and return them as a list suitable for Popen."""
        options = []
        for option,value in kwargs.items():
            if not option.startswith('-'):
                # heuristic for turning key=val pairs into options
                # (fails for commands such as 'find' -- then just use args)
                if len(option) == 1:
                    option = '-' + option         # POSIX style
                else:
                    option = '--' + option        # GNU option
            if value is True:
                options.append(option)
                continue
            elif value is False:
                raise ValueError('A False value is ambiguous for option {0!r}'.format(option))

            if option[:2] == '--':
                options.append(option + '=' + str(value))    # GNU option
            else:
                options.extend((option, str(value)))         # POSIX style
        return options + list(args)