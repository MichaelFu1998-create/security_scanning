def extract_round_trips(transactions,
                        portfolio_value=None):
    """Group transactions into "round trips". First, transactions are
    grouped by day and directionality. Then, long and short
    transactions are matched to create round-trip round_trips for which
    PnL, duration and returns are computed. Crossings where a position
    changes from long to short and vice-versa are handled correctly.

    Under the hood, we reconstruct the individual shares in a
    portfolio over time and match round_trips in a FIFO-order.

    For example, the following transactions would constitute one round trip:
    index                  amount   price    symbol
    2004-01-09 12:18:01    10       50      'AAPL'
    2004-01-09 15:12:53    10       100      'AAPL'
    2004-01-13 14:41:23    -10      100      'AAPL'
    2004-01-13 15:23:34    -10      200       'AAPL'

    First, the first two and last two round_trips will be merged into a two
    single transactions (computing the price via vwap). Then, during
    the portfolio reconstruction, the two resulting transactions will
    be merged and result in 1 round-trip trade with a PnL of
    (150 * 20) - (75 * 20) = 1500.

    Note, that round trips do not have to close out positions
    completely. For example, we could have removed the last
    transaction in the example above and still generated a round-trip
    over 10 shares with 10 shares left in the portfolio to be matched
    with a later transaction.

    Parameters
    ----------
    transactions : pd.DataFrame
        Prices and amounts of executed round_trips. One row per trade.
        - See full explanation in tears.create_full_tear_sheet

    portfolio_value : pd.Series (optional)
        Portfolio value (all net assets including cash) over time.
        Note that portfolio_value needs to beginning of day, so either
        use .shift() or positions.sum(axis='columns') / (1+returns).

    Returns
    -------
    round_trips : pd.DataFrame
        DataFrame with one row per round trip.  The returns column
        contains returns in respect to the portfolio value while
        rt_returns are the returns in regards to the invested capital
        into that partiulcar round-trip.
    """

    transactions = _groupby_consecutive(transactions)
    roundtrips = []

    for sym, trans_sym in transactions.groupby('symbol'):
        trans_sym = trans_sym.sort_index()
        price_stack = deque()
        dt_stack = deque()
        trans_sym['signed_price'] = trans_sym.price * \
            np.sign(trans_sym.amount)
        trans_sym['abs_amount'] = trans_sym.amount.abs().astype(int)
        for dt, t in trans_sym.iterrows():
            if t.price < 0:
                warnings.warn('Negative price detected, ignoring for'
                              'round-trip.')
                continue

            indiv_prices = [t.signed_price] * t.abs_amount
            if (len(price_stack) == 0) or \
               (copysign(1, price_stack[-1]) == copysign(1, t.amount)):
                price_stack.extend(indiv_prices)
                dt_stack.extend([dt] * len(indiv_prices))
            else:
                # Close round-trip
                pnl = 0
                invested = 0
                cur_open_dts = []

                for price in indiv_prices:
                    if len(price_stack) != 0 and \
                       (copysign(1, price_stack[-1]) != copysign(1, price)):
                        # Retrieve first dt, stock-price pair from
                        # stack
                        prev_price = price_stack.popleft()
                        prev_dt = dt_stack.popleft()

                        pnl += -(price + prev_price)
                        cur_open_dts.append(prev_dt)
                        invested += abs(prev_price)

                    else:
                        # Push additional stock-prices onto stack
                        price_stack.append(price)
                        dt_stack.append(dt)

                roundtrips.append({'pnl': pnl,
                                   'open_dt': cur_open_dts[0],
                                   'close_dt': dt,
                                   'long': price < 0,
                                   'rt_returns': pnl / invested,
                                   'symbol': sym,
                                   })

    roundtrips = pd.DataFrame(roundtrips)

    roundtrips['duration'] = roundtrips['close_dt'].sub(roundtrips['open_dt'])

    if portfolio_value is not None:
        # Need to normalize so that we can join
        pv = pd.DataFrame(portfolio_value,
                          columns=['portfolio_value'])\
            .assign(date=portfolio_value.index)

        roundtrips['date'] = roundtrips.close_dt.apply(lambda x:
                                                       x.replace(hour=0,
                                                                 minute=0,
                                                                 second=0))

        tmp = roundtrips.join(pv, on='date', lsuffix='_')

        roundtrips['returns'] = tmp.pnl / tmp.portfolio_value
        roundtrips = roundtrips.drop('date', axis='columns')

    return roundtrips