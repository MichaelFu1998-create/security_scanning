def set_json_value(context, step, current_value, entry_value, is_file):
    """
    Apply a JSON value to a context object
    An implementation of "steps to set a JSON encoding value"
    http://www.w3.org/TR/html-json-forms/#dfn-steps-to-set-a-json-encoding-value
    """

    # TODO: handle is_file

    # Add empty values to array so indexing works like JavaScript
    if isinstance(context, list) and isinstance(step.key, int):
        undefined_count = step.key - len(context) + 1
        if undefined_count > 1000:
            raise ParseException("Too many consecutive empty values!")
        elif undefined_count > 0:
            context += [Undefined()] * undefined_count

    # Step 7: Handle last step
    if step.last:
        if isinstance(current_value, Undefined):
            # Step 7.1: No existing value
            key = step.key
            if isinstance(context, dict) and isinstance(key, int):
                key = str(key)
            if step.append:
                context[key] = [entry_value]
            else:
                context[key] = entry_value
        elif isinstance(current_value, list):
            # Step 7.2: Existing value is an Array, assume multi-valued field
            # and add entry to end.

            # FIXME: What if the other items in the array had explicit keys and
            # this one is supposed to be the "" value?
            # (See step 8.4 and Example 7)
            context[step.key].append(entry_value)

        elif isinstance(current_value, dict) and not is_file:
            # Step 7.3: Existing value is an Object
            return set_json_value(
                context=current_value,
                step=JsonStep(type="object", key="", last=True),
                current_value=current_value.get("", Undefined()),
                entry_value=entry_value,
                is_file=is_file,
            )
        else:
            # Step 7.4: Existing value is a scalar; preserve both values
            context[step.key] = [current_value, entry_value]

        # Step 7.5
        return context

    # Step 8: Handle intermediate steps
    if isinstance(current_value, Undefined):
        # 8.1: No existing value
        if step.next_type == "array":
            context[step.key] = []
        else:
            context[step.key] = {}
        return context[step.key]
    elif isinstance(current_value, dict):
        # Step 8.2: Existing value is an Object
        return get_value(context, step.key, Undefined())
    elif isinstance(current_value, list):
        # Step 8.3: Existing value is an Array
        if step.next_type == "array":
            return current_value
        # Convert array to object to facilitate mixed keys
        obj = {}
        for i, item in enumerate(current_value):
            if not isinstance(item, Undefined):
                obj[str(i)] = item
        context[step.key] = obj
        return obj
    else:
        # 8.4: Existing value is a scalar; convert to Object, preserving
        # current value via an empty key
        obj = {'': current_value}
        context[step.key] = obj
        return obj