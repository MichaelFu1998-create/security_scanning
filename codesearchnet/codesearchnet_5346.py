def one(nodes, or_none=False):
    """
    Assert that there is exactly one node in the give list, and return it.
    """
    if not nodes and or_none:
        return None
    assert len(
        nodes) == 1, 'Expected 1 result. Received %d results.' % (len(nodes))
    return nodes[0]