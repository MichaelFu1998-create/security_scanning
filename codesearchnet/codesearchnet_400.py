def add_closing_transactions(positions, transactions):
    """
    Appends transactions that close out all positions at the end of
    the timespan covered by positions data. Utilizes pricing information
    in the positions DataFrame to determine closing price.

    Parameters
    ----------
    positions : pd.DataFrame
        The positions that the strategy takes over time.
    transactions : pd.DataFrame
        Prices and amounts of executed round_trips. One row per trade.
        - See full explanation in tears.create_full_tear_sheet

    Returns
    -------
    closed_txns : pd.DataFrame
        Transactions with closing transactions appended.
    """

    closed_txns = transactions[['symbol', 'amount', 'price']]

    pos_at_end = positions.drop('cash', axis=1).iloc[-1]
    open_pos = pos_at_end.replace(0, np.nan).dropna()
    # Add closing round_trips one second after the close to be sure
    # they don't conflict with other round_trips executed at that time.
    end_dt = open_pos.name + pd.Timedelta(seconds=1)

    for sym, ending_val in open_pos.iteritems():
        txn_sym = transactions[transactions.symbol == sym]

        ending_amount = txn_sym.amount.sum()

        ending_price = ending_val / ending_amount
        closing_txn = {'symbol': sym,
                       'amount': -ending_amount,
                       'price': ending_price}

        closing_txn = pd.DataFrame(closing_txn, index=[end_dt])
        closed_txns = closed_txns.append(closing_txn)

    closed_txns = closed_txns[closed_txns.amount != 0]

    return closed_txns