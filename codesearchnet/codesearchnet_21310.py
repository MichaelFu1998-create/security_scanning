def f_i18n_citation_type(string, lang="eng"):
    """ Take a string of form %citation_type|passage% and format it for human

    :param string: String of formation %citation_type|passage%
    :param lang: Language to translate to
    :return: Human Readable string

    .. note :: To Do : Use i18n tools and provide real i18n
    """
    s = " ".join(string.strip("%").split("|"))
    return s.capitalize()