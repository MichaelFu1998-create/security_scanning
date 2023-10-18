def _unquote(data):
    """Unquote quoted value from DIGEST-MD5 challenge or response.

    If `data` doesn't start or doesn't end with '"' then return it unchanged,
    remove the quotes and escape backslashes otherwise.

    :Parameters:
        - `data`: a quoted string.
    :Types:
        - `data`: `bytes`

    :return: the unquoted string.
    :returntype: `bytes`
    """
    if not data.startswith(b'"') or not data.endswith(b'"'):
        return data
    return QUOTE_RE.sub(b"\\1", data[1:-1])