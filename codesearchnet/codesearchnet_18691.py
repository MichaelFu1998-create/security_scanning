def parse_callback_args(self, raw_args):
        """This is the method that is called from Script.run(), this is the insertion
        point for parsing all the arguments though on init this will find all args it
        can, so this method pulls already found args from class variables"""
        args = []
        arg_info = self.arg_info
        kwargs = dict(arg_info['optional'])

        parsed_args = []
        unknown_args = getattr(self, "unknown_args", False)
        if unknown_args:
            parsed_args, parsed_unknown_args = self.parse_known_args(raw_args)

            # TODO -- can this be moved to UnknownParser?

            # **kwargs have to be in --key=val form
            # http://stackoverflow.com/a/12807809/5006
            d = defaultdict(list)
            for k, v in ((k.lstrip('-'), v) for k,v in (a.split('=') for a in parsed_unknown_args)):
                d[k].append(v)

            for k in (k for k in d if len(d[k])==1):
                d[k] = d[k][0]

            kwargs.update(d)

        else:
            parsed_args = self.parse_args(raw_args)

        # http://parezcoydigo.wordpress.com/2012/08/04/from-argparse-to-dictionary-in-python-2-7/
        kwargs.update(vars(parsed_args))

        # because of how args works, we need to make sure the kwargs are put in correct
        # order to be passed to the function, otherwise our real *args won't make it
        # to the *args variable
        for k in arg_info['order']:
            args.append(kwargs.pop(k))

        # now that we have the correct order, tack the real *args on the end so they
        # get correctly placed into the function's *args variable
        if arg_info['args']:
            args.extend(kwargs.pop(arg_info['args']))

        return args, kwargs