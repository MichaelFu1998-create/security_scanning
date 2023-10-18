def Normalize(str_):
        """The Normalize(str) function.

        This one also accepts Unicode string input (in the RFC only UTF-8
        strings are used).
        """
        # pylint: disable=C0103
        if isinstance(str_, bytes):
            str_ = str_.decode("utf-8")
        return SASLPREP.prepare(str_).encode("utf-8")