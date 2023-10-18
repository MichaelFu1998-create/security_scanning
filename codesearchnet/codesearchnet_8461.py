def tcase_parse_descr(tcase):
    """Parse descriptions from the the given tcase"""

    descr_short = "SHORT"
    descr_long = "LONG"

    try:
        comment = tcase_comment(tcase)
    except (IOError, OSError, ValueError) as exc:
        comment = []
        cij.err("tcase_parse_descr: failed: %r, tcase: %r" % (exc, tcase))

    comment = [l for l in comment if l.strip()]     # Remove empty lines

    for line_number, line in enumerate(comment):
        if line.startswith("#"):
            comment[line_number] = line[1:]

    if comment:
        descr_short = comment[0]

    if len(comment) > 1:
        descr_long = "\n".join(comment[1:])

    return descr_short, descr_long