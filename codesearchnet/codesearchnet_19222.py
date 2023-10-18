def _assert_contains(haystack, needle, invert, escape=False):
    """
    Test for existence of ``needle`` regex within ``haystack``.

    Say ``escape`` to escape the ``needle`` if you aren't really using the
    regex feature & have special characters in it.
    """
    myneedle = re.escape(needle) if escape else needle
    matched = re.search(myneedle, haystack, re.M)
    if (invert and matched) or (not invert and not matched):
        raise AssertionError("'%s' %sfound in '%s'" % (
            needle,
            "" if invert else "not ",
            haystack
        ))