def parse_segment(text):
    "we expect foo=bar"

    if not len(text):
        return NoopQuerySegment()

    q = QuerySegment()

    # First we need to split the segment into key/value pairs.  This is done
    # by attempting to split the sequence for each equality comparison.  Then
    # discard any that did not split properly.  Then chose the smallest key
    # (greedily chose the first comparator we encounter in the string)
    # followed by the smallest value (greedily chose the largest comparator
    # possible.)

    # translate into [('=', 'foo=bar')]
    equalities = zip(constants.OPERATOR_EQUALITIES, itertools.repeat(text))
    # Translate into [('=', ['foo', 'bar'])]
    equalities = map(lambda x: (x[0], x[1].split(x[0], 1)), equalities)
    # Remove unsplit entries and translate into [('=': ['foo', 'bar'])]
    # Note that the result from this stage is iterated over twice.
    equalities = list(filter(lambda x: len(x[1]) > 1, equalities))
    # Get the smallest key and use the length of that to remove other items
    key_len = len(min((x[1][0] for x in equalities), key=len))
    equalities = filter(lambda x: len(x[1][0]) == key_len, equalities)

    # Get the smallest value length. thus we have the earliest key and the
    # smallest value.
    op, (key, value) = min(equalities, key=lambda x: len(x[1][1]))

    key, directive = parse_directive(key)
    if directive:
        op = constants.OPERATOR_EQUALITY_FALLBACK
        q.directive = directive

    # Process negation.  This comes in both foo.not= and foo!= forms.
    path = key.split(constants.SEP_PATH)
    last = path[-1]

    # Check for !=
    if last.endswith(constants.OPERATOR_NEGATION):
        last = last[:-1]
        q.negated = not q.negated

    # Check for foo.not=
    if last == constants.PATH_NEGATION:
        path.pop(-1)
        q.negated = not q.negated

    q.values = value.split(constants.SEP_VALUE)

    # Check for suffixed operators (foo.gte=bar).  Prioritize suffixed
    # entries over actual equality checks.
    if path[-1] in constants.OPERATOR_SUFFIXES:

        # The case where foo.gte<=bar, which obviously makes no sense.
        if op not in constants.OPERATOR_FALLBACK:
            raise ValueError(
                'Both path-style operator and equality style operator '
                'provided.  Please provide only a single style operator.')

        q.operator = constants.OPERATOR_SUFFIX_MAP[path[-1]]
        path.pop(-1)
    else:
        q.operator = constants.OPERATOR_EQUALITY_MAP[op]

    if not len(path):
        raise ValueError('No attribute navigation path provided.')

    q.path = path

    return q