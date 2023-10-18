def new_account(self, label=None):
        """
        Creates new account, appends it to the :class:`Wallet`'s account list and returns it.

        :param label: account label as `str`
        :rtype: :class:`Account`
        """
        acc, addr = self._backend.new_account(label=label)
        assert acc.index == len(self.accounts)
        self.accounts.append(acc)
        return acc