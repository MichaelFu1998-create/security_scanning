def get_authoryear_from_entry(entry, paren=False):
    """Get and format author-year text from a pybtex entry to emulate
    natbib citations.

    Parameters
    ----------
    entry : `pybtex.database.Entry`
        A pybtex bibliography entry.
    parens : `bool`, optional
        Whether to add parentheses around the year. Default is `False`.

    Returns
    -------
    authoryear : `str`
        The author-year citation text.
    """
    def _format_last(person):
        """Reformat a pybtex Person into a last name.

        Joins all parts of a last name and strips "{}" wrappers.
        """
        return ' '.join([n.strip('{}') for n in person.last_names])

    if len(entry.persons['author']) > 0:
        # Grab author list
        persons = entry.persons['author']
    elif len(entry.persons['editor']) > 0:
        # Grab editor list
        persons = entry.persons['editor']
    else:
        raise AuthorYearError

    try:
        year = entry.fields['year']
    except KeyError:
        raise AuthorYearError

    if paren and len(persons) == 1:
        template = '{author} ({year})'
        return template.format(author=_format_last(persons[0]),
                               year=year)
    elif not paren and len(persons) == 1:
        template = '{author} {year}'
        return template.format(author=_format_last(persons[0]),
                               year=year)
    elif paren and len(persons) == 2:
        template = '{author1} and {author2} ({year})'
        return template.format(author1=_format_last(persons[0]),
                               author2=_format_last(persons[1]),
                               year=year)
    elif not paren and len(persons) == 2:
        template = '{author1} and {author2} {year}'
        return template.format(author1=_format_last(persons[0]),
                               author2=_format_last(persons[1]),
                               year=year)
    elif not paren and len(persons) > 2:
        template = '{author} et al {year}'
        return template.format(author=_format_last(persons[0]),
                               year=year)
    elif paren and len(persons) > 2:
        template = '{author} et al ({year})'
        return template.format(author=_format_last(persons[0]),
                               year=year)