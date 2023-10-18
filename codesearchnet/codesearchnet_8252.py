def account(self):
        """ In oder to obtain the actual
            :class:`account.Account` from this class, you can
            use the ``account`` attribute.
        """
        account = self.account_class(self["owner"], blockchain_instance=self.blockchain)
        # account.refresh()
        return account