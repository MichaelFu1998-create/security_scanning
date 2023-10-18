def tradingStatusDF(symbol=None, token='', version=''):
    '''The Trading status message is used to indicate the current trading status of a security.
     For IEX-listed securities, IEX acts as the primary market and has the authority to institute a trading halt or trading pause in a security due to news dissemination or regulatory reasons.
     For non-IEX-listed securities, IEX abides by any regulatory trading halts and trading pauses instituted by the primary or listing market, as applicable.

    IEX disseminates a full pre-market spin of Trading status messages indicating the trading status of all securities.
     In the spin, IEX will send out a Trading status message with “T” (Trading) for all securities that are eligible for trading at the start of the Pre-Market Session.
     If a security is absent from the dissemination, firms should assume that the security is being treated as operationally halted in the IEX Trading System.

    After the pre-market spin, IEX will use the Trading status message to relay changes in trading status for an individual security. Messages will be sent when a security is:

    Halted
    Paused*
    Released into an Order Acceptance Period*
    Released for trading
    *The paused and released into an Order Acceptance Period status will be disseminated for IEX-listed securities only. Trading pauses on non-IEX-listed securities will be treated simply as a halt.

    https://iexcloud.io/docs/api/#deep-trading-status

    Args:
        symbol (string); Ticker to request
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    x = tradingStatus(symbol, token, version)
    data = []
    for key in x:
        d = x[key]
        d['symbol'] = key
        data.append(d)
    df = pd.DataFrame(data)
    _toDatetime(df)
    return df