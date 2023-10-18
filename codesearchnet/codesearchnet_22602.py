def merge_ordered(ordereds: typing.Iterable[typing.Any]) -> typing.Iterable[typing.Any]:
    """Merge multiple ordered so that within-ordered order is preserved
    """
    seen_set = set()
    add_seen = seen_set.add
    return reversed(tuple(map(
        lambda obj: add_seen(obj) or obj,
        filterfalse(
            seen_set.__contains__,
            chain.from_iterable(map(reversed, reversed(ordereds))),
        ),
    )))