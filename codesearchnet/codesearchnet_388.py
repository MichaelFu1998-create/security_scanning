def daily_txns_with_bar_data(transactions, market_data):
    """
    Sums the absolute value of shares traded in each name on each day.
    Adds columns containing the closing price and total daily volume for
    each day-ticker combination.

    Parameters
    ----------
    transactions : pd.DataFrame
        Prices and amounts of executed trades. One row per trade.
        - See full explanation in tears.create_full_tear_sheet
    market_data : pd.Panel
        Contains "volume" and "price" DataFrames for the tickers
        in the passed positions DataFrames

    Returns
    -------
    txn_daily : pd.DataFrame
        Daily totals for transacted shares in each traded name.
        price and volume columns for close price and daily volume for
        the corresponding ticker, respectively.
    """

    transactions.index.name = 'date'
    txn_daily = pd.DataFrame(transactions.assign(
        amount=abs(transactions.amount)).groupby(
        ['symbol', pd.TimeGrouper('D')]).sum()['amount'])
    txn_daily['price'] = market_data['price'].unstack()
    txn_daily['volume'] = market_data['volume'].unstack()

    txn_daily = txn_daily.reset_index().set_index('date')

    return txn_daily