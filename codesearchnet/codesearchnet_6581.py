def bid(self, trade_id, bid, fast=False):
        """Make a bid.

        :params trade_id: Trade id.
        :params bid: Amount of credits You want to spend.
        :params fast: True for fastest bidding (skips trade status & credits check).
        """
        method = 'PUT'
        url = 'trade/%s/bid' % trade_id

        if not fast:
            rc = self.tradeStatus(trade_id)[0]
            # don't bid if current bid is equal or greater than our max bid
            if rc['currentBid'] >= bid or self.credits < bid:
                return False  # TODO: add exceptions
        data = {'bid': bid}
        try:
            rc = self.__request__(method, url, data=json.dumps(data), params={'sku_b': self.sku_b}, fast=fast)[
                'auctionInfo'][0]
        except PermissionDenied:  # too slow, somebody took it already :-(
            return False
        if rc['bidState'] == 'highest' or (
                rc['tradeState'] == 'closed' and rc['bidState'] == 'buyNow'):  # checking 'tradeState' is required?
            return True
        else:
            return False