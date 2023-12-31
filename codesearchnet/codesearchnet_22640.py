def place_limit_order(self,
                        side,
                        price,
                        size,
                        product_id='BTC-USD',
                        client_oid=None,
                        stp=None,
                        time_in_force=None,
                        cancel_after=None,
                        post_only=None):
    """`<https://docs.exchange.coinbase.com/#orders>`_"""
    return self._place_order(side,
                             product_id=product_id,
                             client_oid=client_oid,
                             type='limit',
                             stp=stp,
                             price=price,
                             size=size,
                             time_in_force=time_in_force,
                             cancel_after=cancel_after,
                             post_only=post_only)