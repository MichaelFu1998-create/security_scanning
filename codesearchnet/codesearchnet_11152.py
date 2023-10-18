def _redo_language(
        self, term, name_mode, rules, final_rules1, final_rules2, concat
    ):
        """Reassess the language of the terms and call the phonetic encoder.

        Uses a split multi-word term.

        Parameters
        ----------
        term : str
            The term to encode via Beider-Morse
        name_mode : str
            The name mode of the algorithm: ``gen`` (default),
            ``ash`` (Ashkenazi), or ``sep`` (Sephardic)
        rules : tuple
            The set of initial phonetic transform regexps
        final_rules1 : tuple
            The common set of final phonetic transform regexps
        final_rules2 : tuple
            The specific set of final phonetic transform regexps
        concat : bool
            A flag to indicate concatenation

        Returns
        -------
        str
            A Beider-Morse phonetic code

        """
        language_arg = self._language(term, name_mode)
        return self._phonetic(
            term,
            name_mode,
            rules,
            final_rules1,
            final_rules2,
            language_arg,
            concat,
        )