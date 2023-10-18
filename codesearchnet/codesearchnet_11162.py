def encode(
        self,
        word,
        language_arg=0,
        name_mode='gen',
        match_mode='approx',
        concat=False,
        filter_langs=False,
    ):
        """Return the Beider-Morse Phonetic Matching encoding(s) of a term.

        Parameters
        ----------
        word : str
            The word to transform
        language_arg : int
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

        Raises
        ------
        ValueError
            Unknown language

        Examples
        --------
        >>> pe = BeiderMorse()
        >>> pe.encode('Christopher')
        'xrQstopir xrQstYpir xristopir xristYpir xrQstofir xrQstYfir
        xristofir xristYfir xristopi xritopir xritopi xristofi xritofir
        xritofi tzristopir tzristofir zristopir zristopi zritopir zritopi
        zristofir zristofi zritofir zritofi'
        >>> pe.encode('Niall')
        'nial niol'
        >>> pe.encode('Smith')
        'zmit'
        >>> pe.encode('Schmidt')
        'zmit stzmit'

        >>> pe.encode('Christopher', language_arg='German')
        'xrQstopir xrQstYpir xristopir xristYpir xrQstofir xrQstYfir
        xristofir xristYfir'
        >>> pe.encode('Christopher', language_arg='English')
        'tzristofir tzrQstofir tzristafir tzrQstafir xristofir xrQstofir
        xristafir xrQstafir'
        >>> pe.encode('Christopher', language_arg='German', name_mode='ash')
        'xrQstopir xrQstYpir xristopir xristYpir xrQstofir xrQstYfir
        xristofir xristYfir'

        >>> pe.encode('Christopher', language_arg='German', match_mode='exact')
        'xriStopher xriStofer xristopher xristofer'

        """
        word = normalize('NFC', text_type(word.strip().lower()))

        name_mode = name_mode.strip().lower()[:3]
        if name_mode not in {'ash', 'sep', 'gen'}:
            name_mode = 'gen'

        if match_mode != 'exact':
            match_mode = 'approx'

        # Translate the supplied language_arg value into an integer
        # representing a set of languages
        all_langs = (
            sum(_LANG_DICT[_] for _ in BMDATA[name_mode]['languages']) - 1
        )
        lang_choices = 0
        if isinstance(language_arg, (int, float, long)):
            lang_choices = int(language_arg)
        elif language_arg != '' and isinstance(language_arg, (text_type, str)):
            for lang in text_type(language_arg).lower().split(','):
                if lang in _LANG_DICT and (_LANG_DICT[lang] & all_langs):
                    lang_choices += _LANG_DICT[lang]
                elif not filter_langs:
                    raise ValueError(
                        'Unknown \''
                        + name_mode
                        + '\' language: \''
                        + lang
                        + '\''
                    )

        # Language choices are either all incompatible with the name mode or
        # no choices were given, so try to autodetect
        if lang_choices == 0:
            language_arg = self._language(word, name_mode)
        else:
            language_arg = lang_choices
        language_arg2 = self._language_index_from_code(language_arg, name_mode)

        rules = BMDATA[name_mode]['rules'][language_arg2]
        final_rules1 = BMDATA[name_mode][match_mode]['common']
        final_rules2 = BMDATA[name_mode][match_mode][language_arg2]

        result = self._phonetic(
            word,
            name_mode,
            rules,
            final_rules1,
            final_rules2,
            language_arg,
            concat,
        )
        result = self._phonetic_numbers(result)

        return result