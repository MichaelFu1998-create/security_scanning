def filter_labels_by_language(labels, language, broader=False):
    '''
    Filter a list of labels, leaving only labels of a certain language.

    :param list labels: A list of :class:`Label`.
    :param str language: An IANA language string, eg. `nl` or `nl-BE`.
    :param boolean broader: When true, will also match `nl-BE` when filtering
        on `nl`. When false, only exact matches are considered.
    '''
    if language == 'any':
        return labels
    if broader:
        language = tags.tag(language).language.format
        return [l for l in labels if tags.tag(l.language).language.format == language]
    else:
        language = tags.tag(language).format
        return [l for l in labels if tags.tag(l.language).format == language]