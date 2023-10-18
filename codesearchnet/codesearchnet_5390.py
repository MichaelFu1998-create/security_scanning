def complete_all(self, pick_up=True, halt_on_manual=True):
        """
        Runs all branches until completion. This is a convenience wrapper
        around :meth:`complete_next`, and the pick_up argument is passed
        along.

        :type  pick_up: bool
        :param pick_up: Passed on to each call of complete_next().
        :type  halt_on_manual: bool
        :param halt_on_manual: When True, this method will not attempt to
                        complete any tasks that have manual=True.
                        See :meth:`SpiffWorkflow.specs.TaskSpec.__init__`
        """
        while self.complete_next(pick_up, halt_on_manual):
            pass