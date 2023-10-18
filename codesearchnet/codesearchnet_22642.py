def _deposit_withdraw(self, type, amount, coinbase_account_id):
    """`<https://docs.exchange.coinbase.com/#depositwithdraw>`_"""
    data = {
      'type':type,
      'amount':amount,
      'coinbase_account_id':coinbase_account_id
    }
    return self._post('transfers', data=data)