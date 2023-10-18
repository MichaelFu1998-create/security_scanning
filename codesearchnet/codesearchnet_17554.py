def get_account_descendants(self, account):
        """
        Retrieves an account's descendants from the general ledger structure
        given the account name.

        :param account_name: The account name.

        :returns: The decendants of the account.
        """

        result = []
        for child in account.accounts:
            self._get_account_and_descendants_(child, result)
        return result