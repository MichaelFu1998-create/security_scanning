def mh_digest (data):
    """
    create a MinHash digest
    """
    num_perm = 512
    m = MinHash(num_perm)

    for d in data:
        m.update(d.encode('utf8'))

    return m