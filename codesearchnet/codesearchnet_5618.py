def opHaltStatusSSE(symbols=None, on_data=None, token='', version=''):
    '''The Exchange may suspend trading of one or more securities on IEX for operational reasons and indicates such operational halt using the Operational halt status message.

    IEX disseminates a full pre-market spin of Operational halt status messages indicating the operational halt status of all securities.
    In the spin, IEX will send out an Operational Halt Message with “N” (Not operationally halted on IEX) for all securities that are eligible for trading at the start of the Pre-Market Session.
    If a security is absent from the dissemination, firms should assume that the security is being treated as operationally halted in the IEX Trading System at the start of the Pre-Market Session.

    After the pre-market spin, IEX will use the Operational halt status message to relay changes in operational halt status for an individual security.

    https://iexcloud.io/docs/api/#deep-operational-halt-status

    Args:
        symbols (string); Tickers to request
        on_data (function): Callback on data
        token (string); Access token
        version (string); API version

    '''
    return _runSSE('op-halt-status', symbols, on_data, token, version)