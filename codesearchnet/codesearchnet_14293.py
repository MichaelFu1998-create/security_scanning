def fix_pylint(line, errors):
    """
    Yield any modified versions of ``line`` needed to address the errors in ``errors``.
    """
    if not errors:
        yield line
        return

    current = PYLINT_EXCEPTION_REGEX.search(line)
    if current:
        original_errors = {disable.strip() for disable in current.group('disables').split(',')}
    else:
        original_errors = set()

    disabled_errors = set(original_errors)

    for error in errors:
        if error.error_name == 'useless-suppression':
            parsed = re.search("""Useless suppression of '(?P<error_name>[^']+)'""", error.error_msg)
            disabled_errors.discard(parsed.group('error_name'))
        elif error.error_name == 'missing-docstring' and error.error_msg == 'Missing module docstring':
            yield format_pylint_disables({error.error_name}).strip() + '\n'
        else:
            disabled_errors.add(error.error_name)

    disable_string = format_pylint_disables(disabled_errors, not disabled_errors <= original_errors)

    if current:
        yield PYLINT_EXCEPTION_REGEX.sub(disable_string, line)
    else:
        yield re.sub(r'($\s*)', disable_string + r'\1', line, count=1)