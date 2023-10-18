def nfkc(data):
    """Do NFKC normalization of Unicode data.

    :Parameters:
        - `data`: list of Unicode characters or Unicode string.

    :return: normalized Unicode string."""
    if isinstance(data, list):
        data = u"".join(data)
    return unicodedata.normalize("NFKC", data)