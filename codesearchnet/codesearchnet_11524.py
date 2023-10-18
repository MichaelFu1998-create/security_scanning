def _post_start(self):
        """Set stdout to non-blocking

        VLC does not always return a newline when reading status so in order to
        be lazy and still use the read API without caring about how much output
        there is we switch stdout to nonblocking mode and just read a large
        chunk of datin order to be lazy and still use the read API without
        caring about how much output there is we switch stdout to nonblocking
        mode and just read a large chunk of data.
        """
        flags = fcntl.fcntl(self._process.stdout, fcntl.F_GETFL)
        fcntl.fcntl(self._process.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)