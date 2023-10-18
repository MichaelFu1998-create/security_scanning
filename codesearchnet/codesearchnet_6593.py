def sendToWatchlist(self, trade_id):
        """Send to watchlist.

        :params trade_id: Trade id.
        """
        method = 'PUT'
        url = 'watchlist'

        data = {'auctionInfo': [{'id': trade_id}]}
        return self.__request__(method, url, data=json.dumps(data))