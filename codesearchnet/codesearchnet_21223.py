def default_chunker(text, getreffs):
    """ This is the default chunker which will resolve the reference giving a callback (getreffs) and a text object with its metadata

    :param text: Text Object representing either an edition or a translation
    :type text: MyCapytains.resources.inventory.Text
    :param getreffs: callback function which retrieves a list of references
    :type getreffs: function

    :return: List of urn references with their human readable version
    :rtype: [(str, str)]
    """
    level = len(text.citation)
    return [tuple([reff.split(":")[-1]]*2) for reff in getreffs(level=level)]