def run(self):
        """
        Execute the model.
        """

        self.prepare_to_run()
        for i in range(0, self.period_count):
            for e in self.entities:
                e.run(self.clock)
            self.clock.tick()