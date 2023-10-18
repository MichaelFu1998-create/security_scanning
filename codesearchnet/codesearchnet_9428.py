def expand_mentions(text, embed_names=True):
    """Searches the given text for mentions and expands them.

    For example:
    "@source.nick" will be expanded to "@<source.nick source.url>".
    """
    if embed_names:
        mention_format = "@<{name} {url}>"
    else:
        mention_format = "@<{url}>"

    def handle_mention(match):
        source = get_source_by_name(match.group(1))
        if source is None:
            return "@{0}".format(match.group(1))
        return mention_format.format(
            name=source.nick,
            url=source.url)

    return short_mention_re.sub(handle_mention, text)