def exec_command(self, cmdstr):
        """
            Execute an x3270 command

            `cmdstr` gets sent directly to the x3270 subprocess on it's stdin.
        """
        if self.is_terminated:
            raise TerminatedError("this TerminalClient instance has been terminated")

        log.debug("sending command: %s", cmdstr)
        c = Command(self.app, cmdstr)
        start = time.time()
        c.execute()
        elapsed = time.time() - start
        log.debug("elapsed execution: {0}".format(elapsed))
        self.status = Status(c.status_line)

        return c