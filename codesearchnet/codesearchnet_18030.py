def do_run_1(self):
        """
        LM run, evaluating 1 step at a time.

        Broyden or eigendirection updates replace full-J updates until
        a full-J update occurs. Does not run with the calculated J (no
        internal run).
        """
        while not self.check_terminate():
            self._has_run = True
            self._run1()
            self._num_iter += 1; self._inner_run_counter += 1