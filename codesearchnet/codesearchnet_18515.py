def sendreturn(gen, value):
    """Send an item into a generator expecting a final return value

    Parameters
    ----------
    gen: ~typing.Generator[T_yield, T_send, T_return]
        the generator to send the value to
    value: T_send
        the value to send

    Raises
    ------
    RuntimeError
        if the generator did not return as expected

    Returns
    -------
    T_return
        the generator's return value
    """
    try:
        gen.send(value)
    except StopIteration as e:
        return stopiter_value(e)
    else:
        raise RuntimeError('generator did not return as expected')