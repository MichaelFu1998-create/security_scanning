def new_fills_report(self,
                       start_date,
                       end_date,
                       account_id=None,
                       product_id='BTC-USD',
                       format=None,
                       email=None):
    """`<https://docs.exchange.coinbase.com/#create-a-new-report>`_"""
    return self._new_report(start_date,
                            'fills',
                            end_date,
                            account_id,
                            product_id,
                            format,
                            email)