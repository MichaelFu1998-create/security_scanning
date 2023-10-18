def remove_account(self, name):
        """
        Remove an account from the account's sub accounts.

        :param name: The name of the account to remove.
        """

        acc_to_remove = None
        for a in self.accounts:
            if a.name == name:
                acc_to_remove = a
        if acc_to_remove is not None:
            self.accounts.remove(acc_to_remove)