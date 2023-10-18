def IterHashes(iterator_size, hash_length=7):
    '''
    Iterator for random hexadecimal hashes

    :param iterator_size:
        Amount of hashes return before this iterator stops.
        Goes on forever if `iterator_size` is negative.

    :param int hash_length:
        Size of each hash returned.

    :return generator(unicode):
    '''
    if not isinstance(iterator_size, int):
        raise TypeError('iterator_size must be integer.')

    count = 0
    while count != iterator_size:
        count += 1
        yield GetRandomHash(hash_length)