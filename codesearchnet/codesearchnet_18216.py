def _parse_field_value(line):
    """ Parse the field and value from a line. """
    if line.startswith(':'):
        # Ignore the line
        return None, None

    if ':' not in line:
        # Treat the entire line as the field, use empty string as value
        return line, ''

    # Else field is before the ':' and value is after
    field, value = line.split(':', 1)

    # If value starts with a space, remove it.
    value = value[1:] if value.startswith(' ') else value

    return field, value