def account_number():
    """Return a random bank account number."""
    account = [random.randint(1, 9) for _ in range(20)]
    return "".join(map(str, account))