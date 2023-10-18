def pylint_amnesty(pylint_output):
    """
    Add ``# pylint: disable`` clauses to add exceptions to all existing pylint errors in a codebase.
    """
    errors = defaultdict(lambda: defaultdict(set))
    for pylint_error in parse_pylint_output(pylint_output):
        errors[pylint_error.filename][pylint_error.linenum].add(pylint_error)

    for file_with_errors in sorted(errors):
        try:
            opened_file = open(file_with_errors)
        except IOError:
            LOG.warning(u"Unable to open %s for edits", file_with_errors, exc_info=True)
        else:
            with opened_file as input_file:
                output_lines = []
                for line_num, line in enumerate(input_file, start=1):
                    output_lines.extend(
                        fix_pylint(
                            line,
                            errors[file_with_errors][line_num]
                        )
                    )

            with open(file_with_errors, 'w') as output_file:
                output_file.writelines(output_lines)