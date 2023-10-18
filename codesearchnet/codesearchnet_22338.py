def _splitHeaders(headers):
    """
    Split an HTTP header whose components are separated with commas.

    Each component is then split on semicolons and the component arguments
    converted into a `dict`.

    @return: `list` of 2-`tuple` of `bytes`, `dict`
    @return: List of header arguments and mapping of component argument names
        to values.
    """
    return [cgi.parse_header(value)
            for value in chain.from_iterable(
                s.split(',') for s in headers
                if s)]