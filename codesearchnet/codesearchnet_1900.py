def varargslist__26(self, fparams, args):
        """
        (2.6, 2.7)
        varargslist: ((fpdef ['=' test] ',')*
                      ('*' NAME [',' '**' NAME] | '**' NAME) |
                      fpdef ['=' test] (',' fpdef ['=' test])* [','])
        """
        for fparam, default_opt in fparams:
            if default_opt:
                equals_loc, default = default_opt
                args.equals_locs.append(equals_loc)
                args.defaults.append(default)
            elif len(args.defaults) > 0:
                error = diagnostic.Diagnostic(
                    "fatal", "non-default argument follows default argument", {},
                    fparam.loc, [args.args[-1].loc.join(args.defaults[-1].loc)])
                self.diagnostic_engine.process(error)

            args.args.append(fparam)

        def fparam_loc(fparam, default_opt):
            if default_opt:
                equals_loc, default = default_opt
                return fparam.loc.join(default.loc)
            else:
                return fparam.loc

        if args.loc is None:
            args.loc = fparam_loc(*fparams[0]).join(fparam_loc(*fparams[-1]))
        elif len(fparams) > 0:
            args.loc = args.loc.join(fparam_loc(*fparams[0]))

        return args