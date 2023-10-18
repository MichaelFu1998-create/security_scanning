def savings_rate(take_home_pay, spending, numtype='float'):
    """
    Calculate net take-home pay including employer retirement savings match
    using the formula laid out by Mr. Money Mustache:
    http://www.mrmoneymustache.com/2015/01/26/calculating-net-worth/

    Args:
        take_home_pay: float or int, monthly take-home pay

        spending: float or int, monthly spending

        numtype: string, 'decimal' or 'float'; the type of number to return.

    Returns:
        your monthly savings rate expressed as a percentage.
    """

    if numtype == 'decimal':
        try:
            return (
                (Decimal(take_home_pay) - Decimal(spending)) / (Decimal(take_home_pay))
            ) * Decimal(100.0)
        # Leave InvalidOperation for backwards compatibility
        except (InvalidOperation, DivisionByZero):
            return Decimal(0.0)
    else:
        try:
            return (
                (float(take_home_pay) - float(spending)) / (float(take_home_pay))
            ) * 100.0
        except (ZeroDivisionError):
            return 0.0