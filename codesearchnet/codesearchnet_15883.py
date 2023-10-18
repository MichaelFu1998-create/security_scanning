def restart(self):
        """Restart an Octave session in a clean state
        """
        if self._engine:
            self._engine.repl.terminate()

        executable = self._executable
        if executable:
            os.environ['OCTAVE_EXECUTABLE'] = executable
        if 'OCTAVE_EXECUTABLE' not in os.environ and 'OCTAVE' in os.environ:
            os.environ['OCTAVE_EXECUTABLE'] = os.environ['OCTAVE']

        self._engine = OctaveEngine(stdin_handler=self._handle_stdin,
                                    logger=self.logger)

        # Add local Octave scripts.
        self._engine.eval('addpath("%s");' % HERE.replace(osp.sep, '/'))