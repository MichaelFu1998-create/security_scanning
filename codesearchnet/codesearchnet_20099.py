def from_yamlfile(cls, fp, selector_handler=None, strict=False, debug=False):
        """
        Create a Parselet instance from a file containing
        the Parsley script as a YAML object

        >>> import parslepy
        >>> with open('parselet.yml') as fp:
        ...     parslepy.Parselet.from_yamlfile(fp)
        ...
        <parslepy.base.Parselet object at 0x2014e50>

        :param file fp: an open file-like pointer containing the Parsley script
        :rtype: :class:`.Parselet`

        Other arguments: same as for :class:`.Parselet` contructor
        """

        return cls.from_yamlstring(fp.read(), selector_handler=selector_handler, strict=strict, debug=debug)