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

        if self.description is None:
            tx_name = self.name
        else:
            tx_name = self.description

        if self._months_executed == 0:
            generalLedger.create_transaction(
                tx_name,
                description='Make a loan',
                tx_date=clock.get_datetime(),
                dt_account=self.bank_account,
                cr_account=self.loan_account,
                source=self.path,
                amount=self.amount)
        else:
            curr_interest_amount = (self._amount_left *
                                    self.interest_rate) / 12.0

            generalLedger.create_transaction(
                tx_name,
                description='Consider interest',
                tx_date=clock.get_datetime(),
                dt_account=self.interest_account,
                cr_account=self.loan_account,
                source=self.path,
                amount=curr_interest_amount)

            generalLedger.create_transaction(
                tx_name,
                description='Pay principle',
                tx_date=clock.get_datetime(),
                dt_account=self.loan_account,
                cr_account=self.bank_account,
                source=self.path,
                amount=self._monthly_payment)

            self._amount_left += curr_interest_amount - self._monthly_payment

        self._months_executed += self.interval