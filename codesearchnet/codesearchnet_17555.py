def _get_account_and_descendants_(self, account, result):
        """
        Returns the account and all of it's sub accounts.

        :param account: The account.
        :param result: The list to add all the accounts to.
        """

        result.append(account)
        for child in account.accounts:
            self._get_account_and_descendants_(child, result)