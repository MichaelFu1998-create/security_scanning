def imap_send(func, gen):
    """Apply a function to all ``send`` values of a generator

    Parameters
    ----------
    func: ~typing.Callable[[T_send], T_mapped]
        the function to apply
    gen: Generable[T_yield, T_mapped, T_return]
        the generator iterable.

    Returns
    -------
    ~typing.Generator[T_yield, T_send, T_return]
        the mapped generator
    """
    gen = iter(gen)
    assert _is_just_started(gen)
    yielder = yield_from(gen)
    for item in yielder:
        with yielder:
            yielder.send(func((yield item)))
    return_(yielder.result)