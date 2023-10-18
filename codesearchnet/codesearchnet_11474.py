def terminate(self):
        """
            terminates the underlying x3270 subprocess. Once called, this
            Emulator instance must no longer be used.
        """
        if not self.is_terminated:
            log.debug("terminal client terminated")
            try:
                self.exec_command(b"Quit")
            except BrokenPipeError:  # noqa
                # x3270 was terminated, since we are just quitting anyway, ignore it.
                pass
            except socket.error as e:
                if e.errno != errno.ECONNRESET:
                    raise
                # this can happen because wc3270 closes the socket before
                # the read() can happen, causing a socket error

            self.app.close()

            self.is_terminated = True