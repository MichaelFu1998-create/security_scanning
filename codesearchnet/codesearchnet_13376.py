def _quote(data):
    """Prepare a string for quoting for DIGEST-MD5 challenge or response.

    Don't add the quotes, only escape '"' and "\\" with backslashes.

    :Parameters:
        - `data`: a raw string.
    :Types:
        - `data`: `bytes`

    :return: `data` with '"' and "\\" escaped using "\\".
    :returntype: `bytes`
    """
    data = data.replace(b'\\', b'\\\\')
    data = data.replace(b'"', b'\\"')
    return data