def validate_account_names(self, names):
        """
        Validates whether the accounts in a list of account names exists.

        :param names: The names of the accounts.

        :returns: The descendants of the account.
        """

        for name in names:
            if self.get_account(name) is None:
                raise ValueError("The account '{}' does not exist in the"
                                 "  general ledger structure.".format(name))