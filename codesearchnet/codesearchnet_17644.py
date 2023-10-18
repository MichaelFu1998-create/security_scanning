def run(self, clock):
        """
        Execute the entity at the current clock cycle.

        :param clock: The clock containing the current execution time and
          period information.
        """

        if clock.timestep_ix >= self.period_count:
            return

        for c in self.components:
            c.run(clock, self.gl)

        self._perform_year_end_procedure(clock)