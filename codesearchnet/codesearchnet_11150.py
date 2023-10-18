def bmpm(
    word,
    language_arg=0,
    name_mode='gen',
    match_mode='approx',
    concat=False,
    filter_langs=False,
):
    """Return the Beider-Morse Phonetic Matching encoding(s) of a term.

    This is a wrapper for :py:meth:`BeiderMorse.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    language_arg : str
        The language of the term; supported values include:

            - ``any``
            - ``arabic``
            - ``cyrillic``
            - ``czech``
            - ``dutch``
            - ``english``
            - ``french``
            - ``german``
            - ``greek``
            - ``greeklatin``
            - ``hebrew``
            - ``hungarian``
            - ``italian``
            - ``latvian``
            - ``polish``
            - ``portuguese``
            - ``romanian``
            - ``russian``
            - ``spanish``
            - ``turkish``

    name_mode : str
        The name mode of the algorithm:

            - ``gen`` -- general (default)
            - ``ash`` -- Ashkenazi
            - ``sep`` -- Sephardic

    match_mode : str
        Matching mode: ``approx`` or ``exact``
    concat : bool
        Concatenation mode
    filter_langs : bool
        Filter out incompatible languages

    Returns
    -------
    tuple
        The Beider-Morse phonetic value(s)

    Examples
    --------
    >>> bmpm('Christopher')
    'xrQstopir xrQstYpir xristopir xristYpir xrQstofir xrQstYfir xristofir
    xristYfir xristopi xritopir xritopi xristofi xritofir xritofi
    tzristopir tzristofir zristopir zristopi zritopir zritopi zristofir
    zristofi zritofir zritofi'
    >>> bmpm('Niall')
    'nial niol'
    >>> bmpm('Smith')
    'zmit'
    >>> bmpm('Schmidt')
    'zmit stzmit'

    >>> bmpm('Christopher', language_arg='German')
    'xrQstopir xrQstYpir xristopir xristYpir xrQstofir xrQstYfir xristofir
    xristYfir'
    >>> bmpm('Christopher', language_arg='English')
    'tzristofir tzrQstofir tzristafir tzrQstafir xristofir xrQstofir
    xristafir xrQstafir'
    >>> bmpm('Christopher', language_arg='German', name_mode='ash')
    'xrQstopir xrQstYpir xristopir xristYpir xrQstofir xrQstYfir xristofir
    xristYfir'

    >>> bmpm('Christopher', language_arg='German', match_mode='exact')
    'xriStopher xriStofer xristopher xristofer'

    """
    return BeiderMorse().encode(
        word, language_arg, name_mode, match_mode, concat, filter_langs
    )