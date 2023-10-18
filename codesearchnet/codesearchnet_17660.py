def run(self, clock, generalLedger):
        """
        Execute the activity at the current clock cycle.

        :param clock: The clock containing the current execution time and
          period information.
        :param generalLedger: The general ledger into which to create the
          transactions.
        """

        if not self._meet_execution_criteria(clock.timestep_ix):
            return

        generalLedger.create_transaction(
            self.description if self.description is not None else self.name,
            description='',
            tx_date=clock.get_datetime(),
            dt_account=self.dt_account,
            cr_account=self.cr_account,
            source=self.path,
            amount=self.amount)