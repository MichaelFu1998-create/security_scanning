def take_home_pay(gross_pay, employer_match, taxes_and_fees, numtype='float'):
    """
    Calculate net take-home pay including employer retirement savings match
    using the formula laid out by Mr. Money Mustache:
    http://www.mrmoneymustache.com/2015/01/26/calculating-net-worth/

    Args:
        gross_pay: float or int, gross monthly pay.

        employer_match: float or int, the 401(k) match from your employer.

        taxes_and_fees: list, taxes and fees that are deducted from your paycheck.

        numtype: string, 'decimal' or 'float'; the type of number to return.

    Returns:
        your monthly take-home pay.
    """
    if numtype == 'decimal':
        return (Decimal(gross_pay) + Decimal(employer_match)) - Decimal(
            sum(taxes_and_fees)
        )
    else:
        return (float(gross_pay) + float(employer_match)) - sum(taxes_and_fees)