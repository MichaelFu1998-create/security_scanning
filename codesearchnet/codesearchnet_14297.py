def parse_json_form(dictionary, prefix=''):
    """
    Parse an HTML JSON form submission as per the W3C Draft spec
    An implementation of "The application/json encoding algorithm"
    http://www.w3.org/TR/html-json-forms/
    """
    # Step 1: Initialize output object
    output = {}
    for name, value in get_all_items(dictionary):
        # TODO: implement is_file flag

        # Step 2: Compute steps array
        steps = parse_json_path(name)

        # Step 3: Initialize context
        context = output

        # Step 4: Iterate through steps
        for step in steps:
            # Step 4.1 Retrieve current value from context
            current_value = get_value(context, step.key, Undefined())

            # Steps 4.2, 4.3: Set JSON value on context
            context = set_json_value(
                context=context,
                step=step,
                current_value=current_value,
                entry_value=value,
                is_file=False,
            )
    # Convert any remaining Undefined array entries to None
    output = clean_undefined(output)
    output = clean_empty_string(output)

    # Account for DRF prefix (not part of JSON form spec)
    result = get_value(output, prefix, Undefined())
    if isinstance(result, Undefined):
        return output
    else:
        return result