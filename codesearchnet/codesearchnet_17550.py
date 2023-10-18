def create_account(self, name, number=None, description=None):
        """
        Create a sub account in the account.

        :param name: The account name.
        :param description: The account description.
        :param number: The account number.

        :returns: The created account.
        """

        new_account = GeneralLedgerAccount(name, description, number,
                                           self.account_type)
        new_account.set_parent_path(self.path)
        self.accounts.append(new_account)
        return new_account