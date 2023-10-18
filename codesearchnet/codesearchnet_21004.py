def with_peer(events):
    """locates ENTER peer for each EXIT object. Convenient when selectively
    filtering out XML markup"""

    stack = []
    for obj in events:
        if obj['type'] == ENTER:
            stack.append(obj)
            yield obj, None
        elif obj['type'] == EXIT:
            yield obj, stack.pop()
        else:
            yield obj, None