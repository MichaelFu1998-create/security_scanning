def _from_jsonlines(cls, lines, selector_handler=None, strict=False, debug=False):
        """
        Interpret input lines as a JSON Parsley script.
        Python-style comment lines are skipped.
        """

        return cls(json.loads(
                "\n".join([l for l in lines if not cls.REGEX_COMMENT_LINE.match(l)])
            ), selector_handler=selector_handler, strict=strict, debug=debug)