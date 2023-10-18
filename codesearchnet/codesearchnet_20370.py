def parse(specifiers):
    """
    Consumes set specifiers as text and forms a generator to retrieve
    the requested ranges.

    @param[in] specifiers
        Expected syntax is from the byte-range-specifier ABNF found in the
        [RFC 2616]; eg. 15-17,151,-16,26-278,15

    @returns
        Consecutive tuples that describe the requested range; eg. (1, 72) or
        (1, 1) [read as 1 to 72 or 1 to 1].
    """
    specifiers = "".join(specifiers.split())
    for specifier in specifiers.split(','):
        if len(specifier) == 0:
            raise ValueError("Range: Invalid syntax; missing specifier.")

        count = specifier.count('-')
        if (count and specifier[0] == '-') or not count:
            # Single specifier; return as a tuple to itself.
            yield int(specifier), int(specifier)
            continue

        specifier = list(map(int, specifier.split('-')))
        if len(specifier) == 2:
            # Range specifier; return as a tuple.
            if specifier[0] < 0 or specifier[1] < 0:
                # Negative indexing is not supported in range specifiers
                # as stated in the HTTP/1.1 Range header specification.
                raise ValueError(
                    "Range: Invalid syntax; negative indexing "
                    "not supported in a range specifier.")

            if specifier[1] < specifier[0]:
                # Range must be for at least one item.
                raise ValueError(
                    "Range: Invalid syntax; stop is less than start.")

            # Return them as a immutable tuple.
            yield tuple(specifier)
            continue

        # Something weird happened.
        raise ValueError("Range: Invalid syntax.")