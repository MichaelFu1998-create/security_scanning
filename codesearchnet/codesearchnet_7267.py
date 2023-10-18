def decode(message, pblite, ignore_first_item=False):
    """Decode pblite to Protocol Buffer message.

    This method is permissive of decoding errors and will log them as warnings
    and continue decoding where possible.

    The first element of the outer pblite list must often be ignored using the
    ignore_first_item parameter because it contains an abbreviation of the name
    of the protobuf message (eg.  cscmrp for ClientSendChatMessageResponseP)
    that's not part of the protobuf.

    Args:
        message: protocol buffer message instance to decode into.
        pblite: list representing a pblite-serialized message.
        ignore_first_item: If True, ignore the item at index 0 in the pblite
            list, making the item at index 1 correspond to field 1 in the
            message.
    """
    if not isinstance(pblite, list):
        logger.warning('Ignoring invalid message: expected list, got %r',
                       type(pblite))
        return
    if ignore_first_item:
        pblite = pblite[1:]
    # If the last item of the list is a dict, use it as additional field/value
    # mappings. This seems to be an optimization added for dealing with really
    # high field numbers.
    if pblite and isinstance(pblite[-1], dict):
        extra_fields = {int(field_number): value for field_number, value
                        in pblite[-1].items()}
        pblite = pblite[:-1]
    else:
        extra_fields = {}
    fields_values = itertools.chain(enumerate(pblite, start=1),
                                    extra_fields.items())
    for field_number, value in fields_values:
        if value is None:
            continue
        try:
            field = message.DESCRIPTOR.fields_by_number[field_number]
        except KeyError:
            # If the tag number is unknown and the value is non-trivial, log a
            # message to aid reverse-engineering the missing field in the
            # message.
            if value not in [[], '', 0]:
                logger.debug('Message %r contains unknown field %s with value '
                             '%r', message.__class__.__name__, field_number,
                             value)
            continue
        if field.label == FieldDescriptor.LABEL_REPEATED:
            _decode_repeated_field(message, field, value)
        else:
            _decode_field(message, field, value)