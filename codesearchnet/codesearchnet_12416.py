def to_atomic(amount):
    """Convert Monero decimal to atomic integer of piconero."""
    if not isinstance(amount, (Decimal, float) + _integer_types):
        raise ValueError("Amount '{}' doesn't have numeric type. Only Decimal, int, long and "
                "float (not recommended) are accepted as amounts.")
    return int(amount * 10**12)