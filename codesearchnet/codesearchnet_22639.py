def _place_order(self,
                   side,
                   product_id='BTC-USD',
                   client_oid=None,
                   type=None,
                   stp=None,
                   price=None,
                   size=None,
                   funds=None,
                   time_in_force=None,
                   cancel_after=None,
                   post_only=None):
    """`<https://docs.exchange.coinbase.com/#orders>`_"""
    data = {
      'side':side,
      'product_id':product_id,
      'client_oid':client_oid,
      'type':type,
      'stp':stp,
      'price':price,
      'size':size,
      'funds':funds,
      'time_in_force':time_in_force,
      'cancel_after':cancel_after,
      'post_only':post_only
    }
    return self._post('orders', data=data)