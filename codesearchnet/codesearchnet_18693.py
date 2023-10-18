def normalize_quiet_arg(self, arg_strings):
        """This is a hack to allow `--quiet` and `--quiet DI` to work correctly,
        basically it goes through all arg_strings and if it finds --quiet it checks
        the next argument to see if it is some combination of DIWEC, if it is then
        it combines it to `--quiet=ARG` and returns the modified arg_strings list

        :param arg_strings: list, the raw arguments
        :returns: list, the arg_strings changed if needed
        """
        if not self.has_injected_quiet(): return arg_strings

        action = self._option_string_actions.get(self.quiet_flags[0])
        if action:
            count = len(arg_strings)
            new_args = []
            i = 0
            while i < count:
                arg_string = arg_strings[i]
                if arg_string in action.option_strings:
                    if (i + 1) < count:
                        narg_string = arg_strings[i + 1]
                        if narg_string in self._option_string_actions:
                            # make sure a flag like -D isn't mistaken for a
                            # --quiet value
                            new_args.append("{}={}".format(arg_string, action.const))

                        elif re.match(r"^\-?[{}]+$".format(action.const), narg_string):
                            new_args.append("{}={}".format(arg_string, narg_string))
                            i += 1

                        else:
                            new_args.append("{}={}".format(arg_string, action.const))

                    else:
                        new_args.append("{}={}".format(arg_string, action.const))

                else:
                    new_args.append(arg_string)

                i += 1

            arg_strings = new_args

        return arg_strings