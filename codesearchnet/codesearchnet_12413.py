def new_address(self, label=None):
        """
        Creates a new address.

        :param label: address label as `str`
        :rtype: :class:`SubAddress <monero.address.SubAddress>`
        """
        return self._backend.new_address(account=self.index, label=label)