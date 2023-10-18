def rlecode_hqx(s):
    """
    Run length encoding for binhex4.
    The CPython implementation does not do run length encoding
    of \x90 characters. This implementation does.
    """
    if not s:
        return ''
    result = []
    prev = s[0]
    count = 1
    # Add a dummy character to get the loop to go one extra round.
    # The dummy must be different from the last character of s.
    # In the same step we remove the first character, which has
    # already been stored in prev.
    if s[-1] == '!':
        s = s[1:] + '?'
    else:
        s = s[1:] + '!'

    for c in s:
        if c == prev and count < 255:
            count += 1
        else:
            if count == 1:
                if prev != '\x90':
                    result.append(prev)
                else:
                    result += ['\x90', '\x00']
            elif count < 4:
                if prev != '\x90':
                    result += [prev] * count
                else:
                    result += ['\x90', '\x00'] * count
            else:
                if prev != '\x90':
                    result += [prev, '\x90', chr(count)]
                else:
                    result += ['\x90', '\x00', '\x90', chr(count)]
            count = 1
            prev = c

    return ''.join(result)