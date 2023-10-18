def _send(self, cmd: str):
        """
        Send a string to the solver.

        :param cmd: a SMTLIBv2 command (ex. (check-sat))
        """
        logger.debug('>%s', cmd)
        try:
            self._proc.stdout.flush()
            self._proc.stdin.write(f'{cmd}\n')
        except IOError as e:
            raise SolverError(str(e))