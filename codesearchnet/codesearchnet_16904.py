def _unescape(s, uri=False):
    """
    Iterative parser for string escapes.
    """
    out = ''
    while len(s) > 0:
        c = s[0]
        if c == '\\':
            # Backslash escape
            esc_c = s[1]

            if esc_c in ('u', 'U'):
                # Unicode escape
                out += six.unichr(int(s[2:6], base=16))
                s = s[6:]
                continue
            else:
                if esc_c == 'b':
                    out += '\b'
                elif esc_c == 'f':
                    out += '\f'
                elif esc_c == 'n':
                    out += '\n'
                elif esc_c == 'r':
                    out += '\r'
                elif esc_c == 't':
                    out += '\t'
                else:
                    if uri and (esc_c == '#'):
                        # \# is passed through with backslash.
                        out += '\\'
                    # Pass through
                    out += esc_c
                s = s[2:]
                continue
        else:
            out += c
            s = s[1:]
    return out