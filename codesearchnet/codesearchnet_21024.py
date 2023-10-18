def quoted(parser=any_token):
    """Parses as much as possible until it encounters a matching closing quote.
    
    By default matches any_token, but can be provided with a more specific parser if required.
    Returns a string
    """
    quote_char = quote()
    value, _ = many_until(parser, partial(one_of, quote_char))
    return build_string(value)