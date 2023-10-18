def _groupby_consecutive(txn, max_delta=pd.Timedelta('8h')):
    """Merge transactions of the same direction separated by less than
    max_delta time duration.

    Parameters
    ----------
    transactions : pd.DataFrame
        Prices and amounts of executed round_trips. One row per trade.
        - See full explanation in tears.create_full_tear_sheet

    max_delta : pandas.Timedelta (optional)
        Merge transactions in the same direction separated by less
        than max_delta time duration.


    Returns
    -------
    transactions : pd.DataFrame

    """
    def vwap(transaction):
        if transaction.amount.sum() == 0:
            warnings.warn('Zero transacted shares, setting vwap to nan.')
            return np.nan
        return (transaction.amount * transaction.price).sum() / \
            transaction.amount.sum()

    out = []
    for sym, t in txn.groupby('symbol'):
        t = t.sort_index()
        t.index.name = 'dt'
        t = t.reset_index()

        t['order_sign'] = t.amount > 0
        t['block_dir'] = (t.order_sign.shift(
            1) != t.order_sign).astype(int).cumsum()
        t['block_time'] = ((t.dt.sub(t.dt.shift(1))) >
                           max_delta).astype(int).cumsum()
        grouped_price = (t.groupby(('block_dir',
                                   'block_time'))
                          .apply(vwap))
        grouped_price.name = 'price'
        grouped_rest = t.groupby(('block_dir', 'block_time')).agg({
            'amount': 'sum',
            'symbol': 'first',
            'dt': 'first'})

        grouped = grouped_rest.join(grouped_price)

        out.append(grouped)

    out = pd.concat(out)
    out = out.set_index('dt')
    return out