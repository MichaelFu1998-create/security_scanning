def _reset(self, constraints=None):
        """Auxiliary method to reset the smtlib external solver to initial defaults"""
        if self._proc is None:
            self._start_proc()
        else:
            if self.support_reset:
                self._send("(reset)")

                for cfg in self._init:
                    self._send(cfg)
            else:
                self._stop_proc()
                self._start_proc()
        if constraints is not None:
            self._send(constraints)