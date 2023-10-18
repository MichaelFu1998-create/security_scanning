def auctionSSE(symbols=None, on_data=None, token='', version=''):
    '''DEEP broadcasts an Auction Information Message every one second between the Lock-in Time and the auction match for Opening and Closing Auctions,
    and during the Display Only Period for IPO, Halt, and Volatility Auctions. Only IEX listed securities are eligible for IEX Auctions.

    https://iexcloud.io/docs/api/#deep-auction

    Args:
        symbols (string); Tickers to request
        on_data (function): Callback on data
        token (string); Access token
        version (string); API version

    '''
    return _runSSE('auction', symbols, on_data, token, version)