def escape_for_xml(data, tags_to_keep=None):
    """Transform & and < to XML valid &amp; and &lt.

    Pass a list of tags as string to enable replacement of
    '<' globally but keep any XML tags in the list.
    """
    data = re.sub("&", "&amp;", data)
    if tags_to_keep:
        data = re.sub(r"(<)(?![\/]?({0})\b)".format("|".join(tags_to_keep)), '&lt;', data)
    else:
        data = re.sub("<", "&lt;", data)
    return data