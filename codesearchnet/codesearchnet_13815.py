def precmd(self, line):
        """
        Allow commands to have a last parameter of 'cookie=somevalue'

        TODO somevalue will be prepended onto any output lines so
        that editors can distinguish output from certain kinds
        of events they have sent.

        :param line:
        :return:
        """
        args = shlex.split(line or "")
        if args and 'cookie=' in args[-1]:
            cookie_index = line.index('cookie=')
            cookie = line[cookie_index + 7:]
            line = line[:cookie_index].strip()
            self.cookie = cookie
        if line.startswith('#'):
            return ''
        elif '=' in line:
            # allow  somevar=somevalue

            # first check if we really mean a command
            cmdname = line.partition(" ")[0]
            if hasattr(self, "do_%s" % cmdname):
                return line

            if not line.startswith("set "):
                return "set " + line
            else:
                return line
        if len(args) and args[0] in self.shortcuts:
            return "%s %s" % (self.shortcuts[args[0]], " ".join(args[1:]))
        else:
            return line