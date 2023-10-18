def get_child_account(self, account_name):
        """
        Retrieves a child account.
        This could be a descendant nested at any level.

        :param account_name: The name of the account to retrieve.

        :returns: The child account, if found, else None.
        """

        if r'/' in account_name:
            accs_in_path = account_name.split(r'/', 1)

            curr_acc = self[accs_in_path[0]]
            if curr_acc is None:
                return None
            return curr_acc.get_child_account(accs_in_path[1])
            pass
        else:
            return self[account_name]