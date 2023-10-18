def send_signal_to_gdb(self, signal_input):
        """Send signal name (case insensitive) or number to gdb subprocess
        gdbmi.send_signal_to_gdb(2)  # valid
        gdbmi.send_signal_to_gdb('sigint')  # also valid
        gdbmi.send_signal_to_gdb('SIGINT')  # also valid

        raises ValueError if signal_input is invalie
        raises NoGdbProcessError if there is no gdb process to send a signal to
        """
        try:
            signal = int(signal_input)
        except Exception:
            signal = SIGNAL_NAME_TO_NUM.get(signal_input.upper())

        if not signal:
            raise ValueError(
                'Could not find signal corresponding to "%s"' % str(signal)
            )

        if self.gdb_process:
            os.kill(self.gdb_process.pid, signal)
        else:
            raise NoGdbProcessError(
                "Cannot send signal to gdb process because no process exists."
            )