def parseaddr(address):
    """Parse an address into a (realname, mailaddr) tuple."""
    a = AddressList(address)
    lst = a.addresslist
    if not lst:
        return (None, None)
    return lst[0]