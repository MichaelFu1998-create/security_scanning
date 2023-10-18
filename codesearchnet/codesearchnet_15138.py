def _get_type(self, values):
        """:return: the type of a knitting pattern set."""
        if TYPE not in values:
            self._error("No pattern type given but should be "
                        "\"{}\"".format(KNITTING_PATTERN_TYPE))
        type_ = values[TYPE]
        if type_ != KNITTING_PATTERN_TYPE:
            self._error("Wrong pattern type. Type is \"{}\" "
                        "but should be \"{}\""
                        "".format(type_, KNITTING_PATTERN_TYPE))
        return type_