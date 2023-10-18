def getaddrlist(self):
        """Parse all addresses.

        Returns a list containing all of the addresses.
        """
        result = []
        ad = self.getaddress()
        while ad:
            result += ad
            ad = self.getaddress()
        return result