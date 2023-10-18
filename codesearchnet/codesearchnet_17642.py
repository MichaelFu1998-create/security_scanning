def run(self, clock, generalLedger):
        """
        Execute the component at the current clock cycle.

        :param clock: The clock containing the current execution time and
          period information.
        :param generalLedger: The general ledger into which to create the
          transactions.
        """

        for c in self.components:
            c.run(clock, generalLedger)
        for a in self.activities:
            a.run(clock, generalLedger)