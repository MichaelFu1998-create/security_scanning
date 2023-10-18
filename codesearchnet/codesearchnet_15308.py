def label(labels=[], language='any', sortLabel=False):
    '''
    Provide a label for a list of labels.

    The items in the list of labels are assumed to be either instances of
    :class:`Label`, or dicts with at least the key `label` in them. These will
    be passed to the :func:`dict_to_label` function.

    This method tries to find a label by looking if there's
    a pref label for the specified language. If there's no pref label,
    it looks for an alt label. It disregards hidden labels.

    While matching languages, preference will be given to exact matches. But,
    if no exact match is present, an inexact match will be attempted. This might
    be because a label in language `nl-BE` is being requested, but only `nl` or
    even `nl-NL` is present. Similarly, when requesting `nl`, a label with
    language `nl-NL` or even `nl-Latn-NL` will also be considered,
    providing no label is present that has an exact match with the
    requested language.

    If language 'any' was specified, all labels will be considered,
    regardless of language.

    To find a label without a specified language, pass `None` as language.

    If a language or None was specified, and no label could be found, this
    method will automatically try to find a label in some other language.

    Finally, if no label could be found, None is returned.

    :param string language: The preferred language to receive the label in. This
        should be a valid IANA language tag.
    :param boolean sortLabel: Should sortLabels be considered or not? If True,
        sortLabels will be preferred over prefLabels. Bear in mind that these
        are still language dependent. So, it's possible to have a different
        sortLabel per language.
    :rtype: A :class:`Label` or `None` if no label could be found.
    '''
    if not labels:
        return None
    if not language:
        language = 'und'
    labels = [dict_to_label(l) for l in labels]
    l = False
    if sortLabel:
        l = find_best_label_for_type(labels, language, 'sortLabel')
    if not l:
        l = find_best_label_for_type(labels, language, 'prefLabel')
    if not l:
        l = find_best_label_for_type(labels, language, 'altLabel')
    if l:
        return l
    else:
        return label(labels, 'any', sortLabel) if language != 'any' else None