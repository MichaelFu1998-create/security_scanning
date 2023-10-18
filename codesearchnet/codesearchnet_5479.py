def expand_partitions(containers, partitions):
    '''
    Validate the partitions of containers. If there are any containers
    not in any partition, place them in an new partition.
    '''

    # filter out holy containers that don't belong
    # to any partition at all
    all_names = frozenset(c.name for c in containers if not c.holy)
    holy_names = frozenset(c.name for c in containers if c.holy)
    neutral_names = frozenset(c.name for c in containers if c.neutral)
    partitions = [frozenset(p) for p in partitions]

    unknown = set()
    holy = set()
    union = set()

    for partition in partitions:
        unknown.update(partition - all_names - holy_names)
        holy.update(partition - all_names)
        union.update(partition)

    if unknown:
        raise BlockadeError('Partitions contain unknown containers: %s' %
                            list(unknown))

    if holy:
        raise BlockadeError('Partitions contain holy containers: %s' %
                            list(holy))

    # put any leftover containers in an implicit partition
    leftover = all_names.difference(union)
    if leftover:
        partitions.append(leftover)

    # we create an 'implicit' partition for the neutral containers
    # in case they are not part of the leftover anyways
    if not neutral_names.issubset(leftover):
        partitions.append(neutral_names)

    return partitions