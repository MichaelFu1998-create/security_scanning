def verify_valid_gdb_subprocess(self):
        """Verify there is a process object, and that it is still running.
        Raise NoGdbProcessError if either of the above are not true."""
        if not self.gdb_process:
            raise NoGdbProcessError("gdb process is not attached")

        elif self.gdb_process.poll() is not None:
            raise NoGdbProcessError(
                "gdb process has already finished with return code: %s"
                % str(self.gdb_process.poll())
            )