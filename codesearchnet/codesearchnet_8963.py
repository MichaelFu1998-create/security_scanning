def __intermediate_address(self, address):
        """
        deletes NetJSON address keys
        """
        for key in self._address_keys:
            if key in address:
                del address[key]
        return address