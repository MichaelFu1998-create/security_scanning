def set_delegate(address=None, pubkey=None, secret=None):
    """Set delegate parameters. Call set_delegate with no arguments to clear."""
    c.DELEGATE['ADDRESS'] = address
    c.DELEGATE['PUBKEY'] = pubkey
    c.DELEGATE['PASSPHRASE'] = secret