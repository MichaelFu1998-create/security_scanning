def create_transaction(self, name, description=None,
                           tx_date=datetime.min.date(),
                           dt_account=None, cr_account=None,
                           source=None, amount=0.00):
        """
        Create a transaction in the general ledger.

        :param name: The transaction's name.
        :param description: The transaction's description.
        :param tx_date: The date of the transaction.
        :param cr_account: The transaction's credit account's name.
        :param dt_account: The transaction's debit account's name.
        :param source: The name of source the transaction originated from.
        :param amount: The transaction amount.

        :returns: The created transaction.
        """

        new_tx = Transaction(name, description, tx_date,
                             dt_account, cr_account, source, amount)
        self.transactions.append(new_tx)
        return new_tx