def applyConsumable(self, item_id, resource_id):
        """Apply consumable on player.

        :params item_id: Item id of player.
        :params resource_id: Resource id of consumable.
        """
        # TODO: catch exception when consumable is not found etc.
        # TODO: multiple players like in quickSell
        method = 'POST'
        url = 'item/resource/%s' % resource_id

        data = {'apply': [{'id': item_id}]}
        self.__request__(method, url, data=json.dumps(data))