def parse(cls, content, is_pyproject=False):
        """
        A convenience method for parsing a TOML-serialized configuration.

        :param content: a TOML string containing a TidyPy configuration
        :type content: str
        :param is_pyproject:
            whether or not the content is (or resembles) a ``pyproject.toml``
            file, where the TidyPy configuration is located within a key named
            ``tool``.
        :type is_pyproject: bool
        :rtype: dict
        """

        parsed = pytoml.loads(content)

        if is_pyproject:
            parsed = parsed.get('tool', {})
        parsed = parsed.get('tidypy', {})

        return parsed