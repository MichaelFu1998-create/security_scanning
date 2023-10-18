def _get_responses_windows(self, timeout_sec):
        """Get responses on windows. Assume no support for select and use a while loop."""
        timeout_time_sec = time.time() + timeout_sec
        responses = []
        while True:
            try:
                self.gdb_process.stdout.flush()
                if PYTHON3:
                    raw_output = self.gdb_process.stdout.readline().replace(
                        b"\r", b"\n"
                    )
                else:
                    raw_output = self.gdb_process.stdout.read().replace(b"\r", b"\n")
                responses += self._get_responses_list(raw_output, "stdout")
            except IOError:
                pass

            try:
                self.gdb_process.stderr.flush()
                if PYTHON3:
                    raw_output = self.gdb_process.stderr.readline().replace(
                        b"\r", b"\n"
                    )
                else:
                    raw_output = self.gdb_process.stderr.read().replace(b"\r", b"\n")
                responses += self._get_responses_list(raw_output, "stderr")
            except IOError:
                pass

            if time.time() > timeout_time_sec:
                break

        return responses