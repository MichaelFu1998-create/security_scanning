def _decode_field(message, field, value):
    """Decode optional or required field."""
    if field.type == FieldDescriptor.TYPE_MESSAGE:
        decode(getattr(message, field.name), value)
    else:
        try:
            if field.type == FieldDescriptor.TYPE_BYTES:
                value = base64.b64decode(value)
            setattr(message, field.name, value)
        except (ValueError, TypeError) as e:
            # ValueError: invalid enum value, negative unsigned int value, or
            # invalid base64
            # TypeError: mismatched type
            logger.warning('Message %r ignoring field %s: %s',
                           message.__class__.__name__, field.name, e)