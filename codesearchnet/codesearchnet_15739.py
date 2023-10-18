def check_digit(num):
    """Return a check digit of the given credit card number.

    Check digit calculated using Luhn algorithm ("modulus 10")
    See: http://www.darkcoding.net/credit-card/luhn-formula/
    """
    sum = 0

    # drop last digit, then reverse the number
    digits = str(num)[:-1][::-1]

    for i, n in enumerate(digits):
        # select all digits at odd positions starting from 1
        if (i + 1) % 2 != 0:
            digit = int(n) * 2
            if digit > 9:
                sum += (digit - 9)
            else:
                sum += digit
        else:
            sum += int(n)

    return ((divmod(sum, 10)[0] + 1) * 10 - sum) % 10