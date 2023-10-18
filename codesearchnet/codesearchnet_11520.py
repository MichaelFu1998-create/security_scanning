def _send_cmd(self, cmd):
        """Write command to remote process
        """
        self._process.stdin.write("{}\n".format(cmd).encode("utf-8"))
        self._process.stdin.flush()