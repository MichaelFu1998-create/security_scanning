def prepare_to_run(self, clock, period_count):
        """
        Prepare the entity for execution.

        :param clock: The clock containing the execution start time and
          execution period information.
        :param period_count: The total amount of periods this activity will be
          requested to be run for.
        """

        self.period_count = period_count

        self._exec_year_end_datetime = clock.get_datetime_at_period_ix(
            period_count)
        self._prev_year_end_datetime = clock.start_datetime
        self._curr_year_end_datetime = clock.start_datetime + relativedelta(
            years=1)

        # Remove all the transactions
        del self.gl.transactions[:]

        for c in self.components:
            c.prepare_to_run(clock, period_count)

        self.negative_income_tax_total = 0