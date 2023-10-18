def quickSell(self, item_id):
        """Quick sell.

        :params item_id: Item id.
        """
        method = 'DELETE'
        url = 'item'

        if not isinstance(item_id, (list, tuple)):
            item_id = (item_id,)
        item_id = (str(i) for i in item_id)
        params = {'itemIds': ','.join(item_id)}
        self.__request__(method, url, params=params)  # {"items":[{"id":280607437106}],"totalCredits":18136}
        return True