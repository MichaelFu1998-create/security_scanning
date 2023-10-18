def irelay(gen, thru):
    """Create a new generator by relaying yield/send interactions
    through another generator

    Parameters
    ----------
    gen: Generable[T_yield, T_send, T_return]
        the original generator
    thru: ~typing.Callable[[T_yield], ~typing.Generator]
        the generator callable through which each interaction is relayed

    Returns
    -------
    ~typing.Generator
        the relayed generator
    """
    gen = iter(gen)
    assert _is_just_started(gen)

    yielder = yield_from(gen)
    for item in yielder:
        with yielder:

            subgen = thru(item)
            subyielder = yield_from(subgen)
            for subitem in subyielder:
                with subyielder:
                    subyielder.send((yield subitem))

            yielder.send(subyielder.result)

    return_(yielder.result)