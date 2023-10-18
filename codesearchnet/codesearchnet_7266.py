def _decode_repeated_field(message, field, value_list):
    """Decode repeated field."""
    if field.type == FieldDescriptor.TYPE_MESSAGE:
        for value in value_list:
            decode(getattr(message, field.name).add(), value)
    else:
        try:
            for value in value_list:
                if field.type == FieldDescriptor.TYPE_BYTES:
                    value = base64.b64decode(value)
                getattr(message, field.name).append(value)
        except (ValueError, TypeError) as e:
            # ValueError: invalid enum value, negative unsigned int value, or
            # invalid base64
            # TypeError: mismatched type
            logger.warning('Message %r ignoring repeated field %s: %s',
                           message.__class__.__name__, field.name, e)
            # Ignore any values already decoded by clearing list
            message.ClearField(field.name)