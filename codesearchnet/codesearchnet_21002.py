def subtree(events):
    """selects sub-tree events"""
    stack = 0
    for obj in events:
        if obj['type'] == ENTER:
            stack += 1
        elif obj['type'] == EXIT:
            if stack == 0:
                break
            stack -= 1
        yield obj