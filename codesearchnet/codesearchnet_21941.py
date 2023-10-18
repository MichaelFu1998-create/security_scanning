def get_field_value_from_context(field_name, context_list):
    """
    Helper to get field value from string path.
    String '<context>' is used to go up on context stack. It just
    can be used at the beginning of path: <context>.<context>.field_name_1
    On the other hand, '<root>' is used to start lookup from first item on context.
    """
    field_path = field_name.split('.')

    if field_path[0] == '<root>':
        context_index = 0
        field_path.pop(0)
    else:
        context_index = -1
        while field_path[0] == '<context>':
            context_index -= 1
            field_path.pop(0)

    try:
        field_value = context_list[context_index]

        while len(field_path):
            field = field_path.pop(0)
            if isinstance(field_value, (list, tuple, ListModel)):
                if field.isdigit():
                    field = int(field)
                field_value = field_value[field]
            elif isinstance(field_value, dict):
                try:
                    field_value = field_value[field]
                except KeyError:
                    if field.isdigit():
                        field = int(field)
                        field_value = field_value[field]
                    else:
                        field_value = None

            else:
                field_value = getattr(field_value, field)

        return field_value
    except (IndexError, AttributeError, KeyError, TypeError):
        return None