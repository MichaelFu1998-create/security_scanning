def load(self, source=None):
        """
        Load the representation of a GameObject from a Python <dict> representing
        the game object.

        :param source: a Python <dict> as detailed above.

        :return:
        """
        if not source:
            raise ValueError("A valid dictionary must be passed as the source_dict")
        if not isinstance(source, dict):
            raise TypeError("A valid dictionary must be passed as the source_dict. {} given.".format(type(source)))

        required_keys = (
            "key",
            "status",
            "ttl",
            "answer",
            "mode",
            "guesses_made")
        if not all(key in source for key in required_keys):
            raise ValueError("The dictionary passed is malformed: {}".format(source))

        _mode = GameMode(**source["mode"])
        self._key = source["key"]
        self._status = source["status"]
        self._ttl = source["ttl"]
        self._answer = DigitWord(*source["answer"], wordtype=_mode.digit_type)
        self._mode = _mode
        self._guesses_made = source["guesses_made"]