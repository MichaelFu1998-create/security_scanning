def tradeStatus(self, trade_id):
        """Return trade status.

        :params trade_id: Trade id.
        """
        method = 'GET'
        url = 'trade/status'

        if not isinstance(trade_id, (list, tuple)):
            trade_id = (trade_id,)
        trade_id = (str(i) for i in trade_id)
        params = {'tradeIds': ','.join(trade_id)}  # multiple trade_ids not tested
        rc = self.__request__(method, url, params=params)
        return [itemParse(i, full=False) for i in rc['auctionInfo']]