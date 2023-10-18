def _create_account_(self, name, number, account_type):
        """
        Create an account in the general ledger structure.

        :param name: The account name.
        :param number: The account number.
        :param account_type: The account type.

        :returns: The created account.
        """

        new_acc = GeneralLedgerAccount(name, None, number, account_type)
        self.accounts.append(new_acc)
        return new_acc