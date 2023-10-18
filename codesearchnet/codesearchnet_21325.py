def get_inventory(self):
        """ Request the api endpoint to retrieve information about the inventory

        :return: Main Collection
        :rtype: Collection
        """
        if self._inventory is not None:
            return self._inventory

        self._inventory = self.resolver.getMetadata()
        return self._inventory