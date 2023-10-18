def move_elements(source, index_to, index_from, length):
    """Move a sub sequence in a list"""

    sublist = [source.pop(index_from) for _ in range(length)]

    for _ in range(length):
        source.insert(index_to, sublist.pop())