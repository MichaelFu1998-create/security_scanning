def remove_direct_link_triples(train, valid, test):
    """Remove direct links in the training sets."""
    pairs = set()
    merged = valid + test
    for t in merged:
        pairs.add((t.head, t.tail))

    filtered = filterfalse(lambda t: (t.head, t.tail) in pairs or (t.tail, t.head) in pairs, train)
    return list(filtered)