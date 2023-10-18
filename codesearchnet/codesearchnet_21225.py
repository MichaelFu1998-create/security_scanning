def line_chunker(text, getreffs, lines=30):
    """ Groups line reference together

    :param text: Text object
    :type text: MyCapytains.resources.text.api
    :param getreffs: Callback function to retrieve text
    :type getreffs: function(level)
    :param lines: Number of lines to use by group
    :type lines: int
    :return: List of grouped urn references with their human readable version
    :rtype: [(str, str)]
    """
    level = len(text.citation)
    source_reffs = [reff.split(":")[-1] for reff in getreffs(level=level)]
    reffs = []
    i = 0
    while i + lines - 1 < len(source_reffs):
        reffs.append(tuple([source_reffs[i]+"-"+source_reffs[i+lines-1], source_reffs[i]]))
        i += lines
    if i < len(source_reffs):
        reffs.append(tuple([source_reffs[i]+"-"+source_reffs[len(source_reffs)-1], source_reffs[i]]))
    return reffs