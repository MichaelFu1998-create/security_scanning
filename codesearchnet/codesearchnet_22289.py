def error_message(self, message, fh=None, prefix="[error]:",
                      suffix="..."):
        """
        print error type message
        if file handle is `sys.stderr`, print color message

        :param str message: message to print
        :param file fh: file handle, default is `sys.stdout`
        :param str prefix: message prefix,default is `[error]`
        :param str suffix: message suffix ,default is '...'
        :return: None
        """

        msg = prefix + message + suffix
        fh = fh or sys.stderr

        if fh is sys.stderr:
            termcolor.cprint(msg, color="red")
        else:
            fh.write(msg)
        pass