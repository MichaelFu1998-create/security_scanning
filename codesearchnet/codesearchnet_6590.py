def watchlistDelete(self, trade_id):
        """Remove cards from watchlist.

        :params trade_id: Trade id.
        """
        method = 'DELETE'
        url = 'watchlist'

        if not isinstance(trade_id, (list, tuple)):
            trade_id = (trade_id,)
        trade_id = (str(i) for i in trade_id)
        params = {'tradeId': ','.join(trade_id)}
        self.__request__(method, url, params=params)  # returns nothing
        return True