def from_yamlstring(cls, s, selector_handler=None, strict=False, debug=False):
        """
        Create a Parselet instance from s (str) containing
        the Parsley script as YAML

        >>> import parslepy
        >>> parsley_string = '''---
            title: h1
            link: a @href
        '''
        >>> p = parslepy.Parselet.from_yamlstring(parsley_string)
        >>> type(p)
        <class 'parslepy.base.Parselet'>
        >>>

        :param string s: a Parsley script as a YAML string
        :rtype: :class:`.Parselet`

        Other arguments: same as for :class:`.Parselet` contructor
        """

        import yaml
        return cls(yaml.load(s), selector_handler=selector_handler, strict=strict, debug=debug)