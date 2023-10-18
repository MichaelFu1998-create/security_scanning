def print_stderr(self, always_print=False):
        """
        Prints the stderr to console - if there is any stdout, otherwise does nothing.
        :param always_print:   print the stderr, even if there is nothing in the buffer (default: false)
        """
        if self.__stderr or always_print:
            self.__echo.critical("--{ STDERR }---" + "-" * 100)
            self.__format_lines_error(self.stderr)
            self.__echo.critical("---------------" + "-" * 100)