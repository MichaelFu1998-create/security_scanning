def warn_message(self, message, fh=None, prefix="[warn]:", suffix="..."):
        """
        print warn type message,
        if file handle is `sys.stdout`, print color message


        :param str message: message to print
        :param file fh: file handle,default is `sys.stdout`
        :param str prefix: message prefix,default is `[warn]`
        :param str suffix: message suffix ,default is `...`
        :return: None
        """

        msg = prefix + message + suffix
        fh = fh or sys.stdout

        if fh is sys.stdout:
            termcolor.cprint(msg, color="yellow")
        else:
            fh.write(msg)

        pass