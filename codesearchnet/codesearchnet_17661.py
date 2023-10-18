def prepare_to_run(self, clock, period_count):
        """
        Prepare the activity for execution.

        :param clock: The clock containing the execution start time and
          execution period information.
        :param period_count: The total amount of periods this activity will be
          requested to be run for.
        """

        super(BasicLoanActivity, self).prepare_to_run(clock, period_count)

        self._months_executed = 0
        self._amount_left = self.amount