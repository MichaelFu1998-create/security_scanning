def toggle(s):
    """
    Toggle back and forth between a name and a tuple representation.

    :param str s: a string which is either a text name, or a tuple-string:
                  a string with three numbers separated by commas

    :returns: if the string was a text name, return a tuple.  If it's a
              tuple-string and it corresponds to a text name, return the text
              name, else return the original tuple-string.
    """
    is_numeric = ',' in s or s.startswith('0x') or s.startswith('#')
    c = name_to_color(s)
    return color_to_name(c) if is_numeric else str(c)