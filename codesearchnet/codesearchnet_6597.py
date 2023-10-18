def packs(self):
        """List all (currently?) available packs."""
        method = 'GET'
        url = 'store/purchaseGroup/cardpack'

        params = {'ppInfo': True}
        return self.__request__(method, url, params=params)