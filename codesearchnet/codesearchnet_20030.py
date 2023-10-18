def list_order_by(l,firstItems):
    """given a list and a list of items to be first, return the list in the
    same order except that it begins with each of the first items."""
    l=list(l)
    for item in firstItems[::-1]: #backwards
        if item in l:
            l.remove(item)
            l.insert(0,item)
    return l