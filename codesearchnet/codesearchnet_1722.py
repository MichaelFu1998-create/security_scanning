def b32decode(s, casefold=False, map01=None):
    """Decode a Base32 encoded string.

    s is the string to decode.  Optional casefold is a flag specifying whether
    a lowercase alphabet is acceptable as input.  For security purposes, the
    default is False.

    RFC 3548 allows for optional mapping of the digit 0 (zero) to the letter O
    (oh), and for optional mapping of the digit 1 (one) to either the letter I
    (eye) or letter L (el).  The optional argument map01 when not None,
    specifies which letter the digit 1 should be mapped to (when map01 is not
    None, the digit 0 is always mapped to the letter O).  For security
    purposes the default is None, so that 0 and 1 are not allowed in the
    input.

    The decoded string is returned.  A TypeError is raised if s were
    incorrectly padded or if there are non-alphabet characters present in the
    string.
    """
    quanta, leftover = divmod(len(s), 8)
    if leftover:
        raise TypeError('Incorrect padding')
    # Handle section 2.4 zero and one mapping.  The flag map01 will be either
    # False, or the character to map the digit 1 (one) to.  It should be
    # either L (el) or I (eye).
    if map01:
        s = s.translate(string.maketrans(b'01', b'O' + map01))
    if casefold:
        s = s.upper()
    # Strip off pad characters from the right.  We need to count the pad
    # characters because this will tell us how many null bytes to remove from
    # the end of the decoded string.
    padchars = 0
    mo = re.search('(?P<pad>[=]*)$', s)
    if mo:
        padchars = len(mo.group('pad'))
        if padchars > 0:
            s = s[:-padchars]
    # Now decode the full quanta
    parts = []
    acc = 0
    shift = 35
    for c in s:
        val = _b32rev.get(c)
        if val is None:
            raise TypeError('Non-base32 digit found')
        acc += _b32rev[c] << shift
        shift -= 5
        if shift < 0:
            parts.append(binascii.unhexlify('%010x' % acc))
            acc = 0
            shift = 35
    # Process the last, partial quanta
    last = binascii.unhexlify('%010x' % acc)
    if padchars == 0:
        last = ''                       # No characters
    elif padchars == 1:
        last = last[:-1]
    elif padchars == 3:
        last = last[:-2]
    elif padchars == 4:
        last = last[:-3]
    elif padchars == 6:
        last = last[:-4]
    else:
        raise TypeError('Incorrect padding')
    parts.append(last)
    return EMPTYSTRING.join(parts)