def copy(self):
        """ Copy the instance and make sure not to use a reference
        """
        return self.__class__(
            amount=self["amount"],
            asset=self["asset"].copy(),
            blockchain_instance=self.blockchain,
        )