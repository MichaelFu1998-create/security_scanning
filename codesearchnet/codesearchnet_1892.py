def Newline(loc=None):
    """A rule that accepts token of kind ``newline`` and returns an empty list."""
    @llrule(loc, lambda parser: ["newline"])
    def rule(parser):
        result = parser._accept("newline")
        if result is unmatched:
            return result
        return []
    return rule