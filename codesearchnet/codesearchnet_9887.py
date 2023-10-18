def _get_responses_unix(self, timeout_sec):
        """Get responses on unix-like system. Use select to wait for output."""
        timeout_time_sec = time.time() + timeout_sec
        responses = []
        while True:
            select_timeout = timeout_time_sec - time.time()
            # I prefer to not pass a negative value to select
            if select_timeout <= 0:
                select_timeout = 0
            events, _, _ = select.select(self.read_list, [], [], select_timeout)
            responses_list = None  # to avoid infinite loop if using Python 2
            try:
                for fileno in events:
                    # new data is ready to read
                    if fileno == self.stdout_fileno:
                        self.gdb_process.stdout.flush()
                        raw_output = self.gdb_process.stdout.read()
                        stream = "stdout"

                    elif fileno == self.stderr_fileno:
                        self.gdb_process.stderr.flush()
                        raw_output = self.gdb_process.stderr.read()
                        stream = "stderr"

                    else:
                        raise ValueError(
                            "Developer error. Got unexpected file number %d" % fileno
                        )

                    responses_list = self._get_responses_list(raw_output, stream)
                    responses += responses_list

            except IOError:  # only occurs in python 2.7
                pass

            if timeout_sec == 0:  # just exit immediately
                break

            elif responses_list and self._allow_overwrite_timeout_times:
                # update timeout time to potentially be closer to now to avoid lengthy wait times when nothing is being output by gdb
                timeout_time_sec = min(
                    time.time() + self.time_to_check_for_additional_output_sec,
                    timeout_time_sec,
                )

            elif time.time() > timeout_time_sec:
                break

        return responses