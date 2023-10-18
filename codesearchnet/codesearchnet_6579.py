def searchDefinition(self, asset_id, start=0, page_size=itemsPerPage['transferMarket'], count=None):
        """Return variations of the given asset id, e.g. IF cards.

        :param asset_id: Asset id / Definition id.
        :param start: (optional) Start page.
        :param count: (optional) Number of definitions you want to request.
        """
        method = 'GET'
        url = 'defid'

        if count:  # backward compatibility, will be removed in future
            page_size = count

        base_id = baseId(asset_id)
        if base_id not in self.players:
            raise FutError(reason='Invalid player asset/definition id.')

        params = {
            'defId': base_id,
            'start': start,
            'type': 'player',
            'count': page_size
        }

        rc = self.__request__(method, url, params=params)

        # try:
        #     return [itemParse({'itemData': i}) for i in rc['itemData']]
        # except:
        #     raise UnknownError('Invalid definition response')
        return [itemParse({'itemData': i}) for i in rc['itemData']]