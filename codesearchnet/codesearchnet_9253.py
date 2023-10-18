def print_traceback(self, always_print=False):
        """
        Prints the traceback to console - if there is any traceback, otherwise does nothing.
        :param always_print:   print the traceback, even if there is nothing in the buffer (default: false)
        """
        if self._exception or always_print:
            self.__echo.critical("--{ TRACEBACK }" + "-" * 100)
            self.__format_lines_error(self.traceback)
            self.__echo.critical("---------------" + "-" * 100)