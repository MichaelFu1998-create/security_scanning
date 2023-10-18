def do_run_2(self):
        """
        LM run evaluating 2 steps (damped and not) and choosing the best.

        After finding the best of 2 steps, runs with that damping + Broyden
        or eigendirection updates, until deciding to do a full-J update.
        Only changes damping after full-J updates.
        """
        while not self.check_terminate():
            self._has_run = True
            self._run2()
            self._num_iter += 1