def prepare_to_run(self, clock, period_count):
        """
        Prepare the component for execution.

        :param clock: The clock containing the execution start time and
          execution period information.
        :param period_count: The total amount of periods this activity will be
          requested to be run for.
        """

        for c in self.components:
            c.prepare_to_run(clock, period_count)
        for a in self.activities:
            a.prepare_to_run(clock, period_count)