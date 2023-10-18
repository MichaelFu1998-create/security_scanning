def prepare_to_run(self, clock, period_count):
        """
        Prepare the activity for execution.

        :param clock: The clock containing the execution start time and
          execution period information.
        :param period_count: The total amount of periods this activity will be
          requested to be run for.
        """

        if self.start_period_ix == -1 and self.start_datetime != datetime.min:
            # Set the Start period index
            for i in range(0, period_count):
                if clock.get_datetime_at_period_ix(i) > self.start_datetime:
                    self.start_period_ix = i
                    break
        if self.start_period_ix == -1:
            self.start_period_ix = 0
        if self.period_count == -1 and self.end_datetime != datetime.max:
            # Set the Start date
            for i in range(0, period_count):
                if clock.get_datetime_at_period_ix(i) > self.end_datetime:
                    self.period_count = i - self.start_period_ix
                    break
        if self.period_count != -1:
            self.end_period_ix = self.start_period_ix + self.period_count
        else:
            self.end_period_ix = self.start_period_ix + period_count