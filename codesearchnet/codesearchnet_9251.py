def print_stdout(self, always_print=False):
        """
        Prints the stdout to console - if there is any stdout, otherwise does nothing.
        :param always_print:   print the stdout, even if there is nothing in the buffer (default: false)
        """
        if self.__stdout or always_print:
            self.__echo.info("--{ STDOUT }---" + "-" * 100)
            self.__format_lines_info(self.stdout)
            self.__echo.info("---------------" + "-" * 100)