def _language(self, name, name_mode):
        """Return the best guess language ID for the word and language choices.

        Parameters
        ----------
        name : str
            The term to guess the language of
        name_mode : str
            The name mode of the algorithm: ``gen`` (default),
            ``ash`` (Ashkenazi), or ``sep`` (Sephardic)

        Returns
        -------
        int
            Language ID

        """
        name = name.strip().lower()
        rules = BMDATA[name_mode]['language_rules']
        all_langs = (
            sum(_LANG_DICT[_] for _ in BMDATA[name_mode]['languages']) - 1
        )
        choices_remaining = all_langs
        for rule in rules:
            letters, languages, accept = rule
            if search(letters, name) is not None:
                if accept:
                    choices_remaining &= languages
                else:
                    choices_remaining &= (~languages) % (all_langs + 1)
        if choices_remaining == L_NONE:
            choices_remaining = L_ANY
        return choices_remaining