def from_jsonstring(cls, s, selector_handler=None, strict=False, debug=False):
        """
        Create a Parselet instance from s (str) containing
        the Parsley script as JSON

        >>> import parslepy
        >>> parsley_string = '{ "title": "h1", "link": "a @href"}'
        >>> p = parslepy.Parselet.from_jsonstring(parsley_string)
        >>> type(p)
        <class 'parslepy.base.Parselet'>
        >>>

        :param string s: a Parsley script as a JSON string
        :rtype: :class:`.Parselet`

        Other arguments: same as for :class:`.Parselet` contructor
        """

        return cls._from_jsonlines(s.split("\n"),
            selector_handler=selector_handler, strict=strict, debug=debug)