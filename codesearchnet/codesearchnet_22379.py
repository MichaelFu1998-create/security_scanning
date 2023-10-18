def check_readable(self, timeout):
        """
        Poll ``self.stdout`` and return True if it is readable.

        :param float timeout: seconds to wait I/O
        :return: True if readable, else False
        :rtype: boolean
        """
        rlist, wlist, xlist = select.select([self._stdout], [], [], timeout)
        return bool(len(rlist))