def _start_proc(self):
        """Spawns z3 solver process"""
        assert '_proc' not in dir(self) or self._proc is None
        try:
            self._proc = Popen(shlex.split(self._command), stdin=PIPE, stdout=PIPE, bufsize=0, universal_newlines=True)
        except OSError as e:
            print(e, "Probably too many cached expressions? visitors._cache...")
            # Z3 was removed from the system in the middle of operation
            raise Z3NotFoundError  # TODO(mark) don't catch this exception in two places

        # run solver specific initializations
        for cfg in self._init:
            self._send(cfg)