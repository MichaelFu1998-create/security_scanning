def is_equal(a, b):
    """ a constant time comparison implementation taken from
        http://codahale.com/a-lesson-in-timing-attacks/ and
        Django's `util` module https://github.com/django/django/blob/master/django/utils/crypto.py#L82
    """
    if len(a) != len(b):
        return False

    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)
    return result == 0