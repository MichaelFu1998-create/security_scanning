def _stop_proc(self):
        """
        Stops the z3 solver process by:
        - sending an exit command to it,
        - sending a SIGKILL signal,
        - waiting till the process terminates (so we don't leave a zombie process)
        """
        if self._proc is None:
            return
        if self._proc.returncode is None:
            try:
                self._send("(exit)")
            except (SolverError, IOError) as e:
                # z3 was too fast to close
                logger.debug(str(e))
            finally:
                try:
                    self._proc.stdin.close()
                except IOError as e:
                    logger.debug(str(e))
                try:
                    self._proc.stdout.close()
                except IOError as e:
                    logger.debug(str(e))
                self._proc.kill()
                # Wait for termination, to avoid zombies.
                self._proc.wait()

        self._proc: Popen = None