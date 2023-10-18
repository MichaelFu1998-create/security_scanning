def future_value(present_value, annual_rate, periods_per_year, years):
    """
    Calculates the future value of money invested at an anual interest rate,
    x times per year, for a given number of years.

    Args:
        present_value: int or float, the current value of the money (principal).

        annual_rate: float 0 to 1 e.g., .5 = 50%), the interest rate paid out.

        periods_per_year: int, the number of times money is invested per year.

        years: int, the number of years invested.

    Returns:
        Float, the future value of the money invested with compound interest.
    """

    # The nominal interest rate per period (rate) is how much interest you earn during a
    # particular length of time, before accounting for compounding. This is typically
    # expressed as a percentage.
    rate_per_period = annual_rate / float(periods_per_year)

    # How many periods in the future the calculation is for.
    periods = periods_per_year * years

    return present_value * (1 + rate_per_period) ** periods