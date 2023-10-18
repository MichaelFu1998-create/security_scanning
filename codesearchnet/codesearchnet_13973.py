def next_event(block=False, timeout=None):
    """
    Get the next available event or None

    :param block:
    :param timeout:
    :return: None or (event, data)
    """
    try:
        return channel.listen(block=block, timeout=timeout).next()['data']
    except StopIteration:
        return None