def find_args(self):
        """when a new parser is created this is the method that is called from its
        __init__ method to find all the arguments"""
        arg_info = self.arg_info
        main = self.callback
        cbi = CallbackInspect(main)
        all_arg_names = set()
        decorator_args = cbi.args
        args, args_name, kwargs_name, args_defaults = cbi.argspec

        arg_info['order'] = args
        default_offset = len(args) - len(args_defaults)
        #pout.v(args, args_name, kwargs_name, args_defaults, default_offset)
        #pout.v(args, decorator_args)

        # build a list of potential *args, basically, if an arg_name matches exactly
        # then it is an *arg and we shouldn't mess with it in the function
        comp_args = set()
        for da in decorator_args:
            comp_args.update(da[0])

        for i, arg_name in enumerate(args):
            if arg_name in comp_args: continue

            a = ScriptKwarg(arg_name)

            # set the default if it is available
            default_i = i - default_offset
            if default_i >= 0:
                na = args_defaults[default_i]
                a.set_default(na)

            a.merge_from_list(decorator_args)

            if a.required:
                arg_info['required'].append(a.name)

            else:
                arg_info['optional'][a.name] = a.default

            #pout.v(a.parser_args, a.parser_kwargs)
            all_arg_names |= a.parser_args

            # if the callback arg is just a value, respect the parent parser's config
            if "default" not in a.parser_kwargs \
            and "action" not in a.parser_kwargs \
            and "choices" not in a.parser_kwargs:
                keys = self._option_string_actions.keys()
                found_arg = False
                for pa in a.parser_args:
                    if pa in keys:
                        found_arg = True
                        break

                if not found_arg:
                    self.add_argument(*a.parser_args, **a.parser_kwargs)

            else:
                # we want to override parent parser
                self.add_argument(*a.parser_args, **a.parser_kwargs)

        self.unknown_args = False
        if self.add_help:
            if args_name:
                a = ScriptArg(args_name, nargs='*')
                a.merge_from_list(decorator_args)
                all_arg_names |= a.parser_args
                self.add_argument(*a.parser_args, **a.parser_kwargs)
                arg_info['args'] = args_name

            if kwargs_name:
                self.unknown_args = True
                arg_info['kwargs'] = kwargs_name

        # pick up any stragglers
        for da, dkw in decorator_args:
            if da[0] not in all_arg_names:
                arg_name = da[0]
                if arg_name.startswith("-"):
                    a = ScriptKwarg(*da)
                else:
                    a = ScriptArg(*da)

                a.merge_kwargs(dkw)
                self.add_argument(*a.parser_args, **a.parser_kwargs)

        self.arg_info = arg_info