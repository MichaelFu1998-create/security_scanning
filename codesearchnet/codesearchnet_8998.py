def versioncmp(v1, v2):
    """Compares two objects, x and y, and returns an integer according to the
    outcome. The return value is negative if x < y, zero if x == y and
    positive if x > y.

    :param v1: The first object to compare.
    :param v2: The second object to compare.

    :returns: -1, 0 or 1.
    :rtype: :obj:`int`
    """
    def normalize(v):
        """Removes leading zeroes from right of a decimal point from v and
        returns an array of values separated by '.'

        :param v: The data to normalize.

        :returns: An list representation separated by '.' with all leading
            zeroes stripped.
        :rtype: :obj:`list`
        """
        return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split(".")]
    try:
        return cmp(normalize(v1), normalize(v2))
    except NameError:
        return (normalize(v1) > normalize(v2)) - (
            normalize(v1) < normalize(v2))