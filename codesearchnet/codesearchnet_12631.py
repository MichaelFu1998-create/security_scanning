def has_digit(string_or_list, sep="_"):
    """
    Given a string or a list will return true if the last word or
    element is a digit.  sep is used when a string is given to know
    what separates one word from another.
    """
    if isinstance(string_or_list, (tuple, list)):
        list_length = len(string_or_list)
        if list_length:
            return six.text_type(string_or_list[-1]).isdigit()
        else:
            return False
    else:
        return has_digit(string_or_list.split(sep))