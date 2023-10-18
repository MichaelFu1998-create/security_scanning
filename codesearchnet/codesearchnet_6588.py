def sell(self, item_id, bid, buy_now, duration=3600, fast=False):
        """Start auction. Returns trade_id.

        :params item_id: Item id.
        :params bid: Stard bid.
        :params buy_now: Buy now price.
        :params duration: Auction duration in seconds (Default: 3600).
        """
        method = 'POST'
        url = 'auctionhouse'

        # TODO: auto send to tradepile
        data = {'buyNowPrice': buy_now, 'startingBid': bid, 'duration': duration, 'itemData': {'id': item_id}}
        rc = self.__request__(method, url, data=json.dumps(data), params={'sku_b': self.sku_b})
        if not fast:  # tradeStatus check like webapp do
            self.tradeStatus(rc['id'])
        return rc['id']