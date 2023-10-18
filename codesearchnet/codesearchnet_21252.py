def _from_parts(cls, args, init=True):
        """
        Strip \\?\ prefix in init phase
        """
        if args:
            args = list(args)
            if isinstance(args[0], WindowsPath2):
                args[0] = args[0].path
            elif args[0].startswith("\\\\?\\"):
                args[0] = args[0][4:]
            args = tuple(args)
        return super(WindowsPath2, cls)._from_parts(args, init)