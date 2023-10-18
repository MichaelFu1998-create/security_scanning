def prepare_to_run(self):
        """
        Prepare the model for execution.
        """

        self.clock.reset()
        for e in self.entities:
            e.prepare_to_run(self.clock, self.period_count)