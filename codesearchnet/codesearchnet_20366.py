def split_segments(text, closing_paren=False):
    """Return objects representing segments."""
    buf = StringIO()

    # The segments we're building, and the combinators used to combine them.
    # Note that after this is complete, this should be true:
    # len(segments) == len(combinators) + 1
    # Thus we can understand the relationship between segments and combinators
    # like so:
    #  s1 (c1) s2 (c2) s3 (c3) where sN are segments and cN are combination
    # functions.
    # TODO: Figure out exactly where the querystring died and post cool
    # error messages about it.
    segments = []
    combinators = []

    # A flag dictating if the last character we processed was a group.
    # This is used to determine if the next character (being a combinator)
    # is allowed to
    last_group = False

    # The recursive nature of this function relies on keeping track of the
    # state of iteration.  This iterator will be passed down to recursed calls.
    iterator = iter(text)

    # Detection for exclamation points.  only matters for this situation:
    # foo=bar&!(bar=baz)
    last_negation = False

    for character in iterator:
        if character in COMBINATORS:

            if last_negation:
                buf.write(constants.OPERATOR_NEGATION)

            # The string representation of our segment.
            val = buf.getvalue()
            reset_stringio(buf)

            if not last_group and not len(val):
                raise ValueError('Unexpected %s.' % character)

            # When a group happens, the previous value is empty.
            if len(val):
                segments.append(parse_segment(val))

            combinators.append(COMBINATORS[character])

        elif character == constants.GROUP_BEGIN:
            # Recursively go into the next group.

            if buf.tell():
                raise ValueError('Unexpected %s' % character)

            seg = split_segments(iterator, True)

            if last_negation:
                seg = UnarySegmentCombinator(seg)

            segments.append(seg)

            # Flag that the last entry was a grouping, so that we don't panic
            # when the next character is a logical combinator
            last_group = True
            continue

        elif character == constants.GROUP_END:
            # Build the segment for anything remaining, and then combine
            # all the segments.
            val = buf.getvalue()

            # Check for unbalanced parens or an empty thing: foo=bar&();bar=baz
            if not buf.tell() or not closing_paren:
                raise ValueError('Unexpected %s' % character)

            segments.append(parse_segment(val))
            return combine(segments, combinators)

        elif character == constants.OPERATOR_NEGATION and not buf.tell():
            last_negation = True
            continue

        else:
            if last_negation:
                buf.write(constants.OPERATOR_NEGATION)
            if last_group:
                raise ValueError('Unexpected %s' % character)
            buf.write(character)

        last_negation = False
        last_group = False
    else:
        # Check and see if the iterator exited early (unbalanced parens)
        if closing_paren:
            raise ValueError('Expected %s.' % constants.GROUP_END)

        if not last_group:
            # Add the final segment.
            segments.append(parse_segment(buf.getvalue()))

    # Everything completed normally, combine all the segments into one
    # and return them.
    return combine(segments, combinators)