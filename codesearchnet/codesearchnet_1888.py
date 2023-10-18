def Seq(first_rule, *rest_of_rules, **kwargs):
    """
    A rule that accepts a sequence of tokens satisfying ``rules`` and returns a tuple
    containing their return values, or None if the first rule was not satisfied.
    """
    @llrule(kwargs.get("loc", None), first_rule.expected)
    def rule(parser):
        result = first_rule(parser)
        if result is unmatched:
            return result

        results = [result]
        for rule in rest_of_rules:
            result = rule(parser)
            if result is unmatched:
                return result
            results.append(result)
        return tuple(results)
    return rule