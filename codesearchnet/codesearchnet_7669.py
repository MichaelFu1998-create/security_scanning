def pass_from_pipe(cls):
        """Return password from pipe if not on TTY, else False.
        """
        is_pipe = not sys.stdin.isatty()
        return is_pipe and cls.strip_last_newline(sys.stdin.read())