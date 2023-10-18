def write(
        self,
        mi_cmd_to_write,
        timeout_sec=DEFAULT_GDB_TIMEOUT_SEC,
        raise_error_on_timeout=True,
        read_response=True,
    ):
        """Write to gdb process. Block while parsing responses from gdb for a maximum of timeout_sec.

        Args:
            mi_cmd_to_write (str or list): String to write to gdb. If list, it is joined by newlines.
            timeout_sec (float): Maximum number of seconds to wait for response before exiting. Must be >= 0.
            raise_error_on_timeout (bool): If read_response is True, raise error if no response is received
            read_response (bool): Block and read response. If there is a separate thread running,
            this can be false, and the reading thread read the output.
        Returns:
            List of parsed gdb responses if read_response is True, otherwise []
        Raises:
            NoGdbProcessError if there is no gdb subprocess running
            TypeError if mi_cmd_to_write is not valid
        """
        self.verify_valid_gdb_subprocess()
        if timeout_sec < 0:
            self.logger.warning("timeout_sec was negative, replacing with 0")
            timeout_sec = 0

        # Ensure proper type of the mi command
        if type(mi_cmd_to_write) in [str, unicode]:
            pass
        elif type(mi_cmd_to_write) == list:
            mi_cmd_to_write = "\n".join(mi_cmd_to_write)
        else:
            raise TypeError(
                "The gdb mi command must a be str or list. Got "
                + str(type(mi_cmd_to_write))
            )

        self.logger.debug("writing: %s", mi_cmd_to_write)

        if not mi_cmd_to_write.endswith("\n"):
            mi_cmd_to_write_nl = mi_cmd_to_write + "\n"
        else:
            mi_cmd_to_write_nl = mi_cmd_to_write

        if USING_WINDOWS:
            # select not implemented in windows for pipes
            # assume it's always ready
            outputready = [self.stdin_fileno]
        else:
            _, outputready, _ = select.select([], self.write_list, [], timeout_sec)
        for fileno in outputready:
            if fileno == self.stdin_fileno:
                # ready to write
                self.gdb_process.stdin.write(mi_cmd_to_write_nl.encode())
                # don't forget to flush for Python3, otherwise gdb won't realize there is data
                # to evaluate, and we won't get a response
                self.gdb_process.stdin.flush()
            else:
                self.logger.error("got unexpected fileno %d" % fileno)

        if read_response is True:
            return self.get_gdb_response(
                timeout_sec=timeout_sec, raise_error_on_timeout=raise_error_on_timeout
            )

        else:
            return []