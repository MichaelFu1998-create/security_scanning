def f_i18n_iso(isocode, lang="eng"):
    """ Replace isocode by its language equivalent

    :param isocode: Three character long language code
    :param lang: Lang in which to return the language name
    :return: Full Text Language Name
    """
    if lang not in flask_nemo._data.AVAILABLE_TRANSLATIONS:
        lang = "eng"

    try:
        return flask_nemo._data.ISOCODES[isocode][lang]
    except KeyError:
        return "Unknown"