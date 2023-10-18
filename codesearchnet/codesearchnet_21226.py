def level_chunker(text, getreffs, level=1):
    """ Chunk a text at the passage level

    :param text: Text object
    :type text: MyCapytains.resources.text.api
    :param getreffs: Callback function to retrieve text
    :type getreffs: function(level)
    :return: List of urn references with their human readable version
    :rtype: [(str, str)]
    """
    references = getreffs(level=level)
    return [(ref.split(":")[-1], ref.split(":")[-1]) for ref in references]