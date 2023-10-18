def checksum_from_sha1(value):
    """
    Return an spdx.checksum.Algorithm instance representing the SHA1
    checksum or None if does not match CHECKSUM_RE.
    """
    # More constrained regex at lexer level
    CHECKSUM_RE = re.compile('SHA1:\s*([\S]+)', re.UNICODE)
    match = CHECKSUM_RE.match(value)
    if match:
        return checksum.Algorithm(identifier='SHA1', value=match.group(1))
    else:
        return None