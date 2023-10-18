def find_best_label_for_type(labels, language, labeltype):
    '''
    Find the best label for a certain labeltype.

    :param list labels: A list of :class:`Label`.
    :param str language: An IANA language string, eg. `nl` or `nl-BE`.
    :param str labeltype: Type of label to look for, eg. `prefLabel`.
    '''
    typelabels = [l for l in labels if l.type == labeltype]
    if not typelabels:
        return False
    if language == 'any':
        return typelabels[0]
    exact = filter_labels_by_language(typelabels, language)
    if exact:
        return exact[0]
    inexact = filter_labels_by_language(typelabels, language, True)
    if inexact:
        return inexact[0]
    return False