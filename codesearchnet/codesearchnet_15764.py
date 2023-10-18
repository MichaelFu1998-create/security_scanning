def password(at_least=6, at_most=12, lowercase=True,
             uppercase=True, digits=True, spaces=False, punctuation=False):
    """Return a random string for use as a password."""
    return text(at_least=at_least, at_most=at_most, lowercase=lowercase,
                uppercase=uppercase, digits=digits, spaces=spaces,
                punctuation=punctuation)