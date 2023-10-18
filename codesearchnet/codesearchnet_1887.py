def Expect(inner_rule, loc=None):
    """A rule that executes ``inner_rule`` and emits a diagnostic error if it returns None."""
    @llrule(loc, inner_rule.expected)
    def rule(parser):
        result = inner_rule(parser)
        if result is unmatched:
            expected = reduce(list.__add__, [rule.expected(parser) for rule in parser._errrules])
            expected = list(sorted(set(expected)))

            if len(expected) > 1:
                expected = " or ".join([", ".join(expected[0:-1]), expected[-1]])
            elif len(expected) == 1:
                expected = expected[0]
            else:
                expected = "(impossible)"

            error_tok = parser._tokens[parser._errindex]
            error = diagnostic.Diagnostic(
                "fatal", "unexpected {actual}: expected {expected}",
                {"actual": error_tok.kind, "expected": expected},
                error_tok.loc)
            parser.diagnostic_engine.process(error)
        return result
    return rule