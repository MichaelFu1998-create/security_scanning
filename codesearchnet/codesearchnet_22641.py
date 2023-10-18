def place_market_order(self,
                         side,
                         product_id='BTC-USD',
                         size=None,
                         funds=None,
                         client_oid=None,
                         stp=None):
    """`<https://docs.exchange.coinbase.com/#orders>`_"""
    return self._place_order(type='market',
                             side=size,
                             product_id=product_id,
                             size=size,
                             funds=funds,
                             client_oid=client_oid,
                             stp=stp)