def parse_pylint_output(pylint_output):
    """
    Parse the pylint output-format=parseable lines into PylintError tuples.
    """
    for line in pylint_output:
        if not line.strip():
            continue

        if line[0:5] in ("-"*5, "*"*5):
            continue

        parsed = PYLINT_PARSEABLE_REGEX.search(line)
        if parsed is None:
            LOG.warning(
                u"Unable to parse %r. If this is a lint failure, please re-run pylint with the "
                u"--output-format=parseable option, otherwise, you can ignore this message.",
                line
            )
            continue

        parsed_dict = parsed.groupdict()
        parsed_dict['linenum'] = int(parsed_dict['linenum'])
        yield PylintError(**parsed_dict)