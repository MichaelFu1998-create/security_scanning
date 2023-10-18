def get_historic_trades(self, start, end, granularity, product_id='BTC-USD'):
    """`<https://docs.exchange.coinbase.com/#get-historic-rates>`_

    :param start: either datetime.datetime or str in ISO 8601
    :param end: either datetime.datetime or str in ISO 8601
    :pram int granularity: desired timeslice in seconds
    :returns: desired data

    """
    params = {
      'start':self._format_iso_time(start),
      'end':self._format_iso_time(end),
      'granularity':granularity
    }
    return self._get('products', product_id, 'candles', params=params)