def record_add_field(rec, tag, ind1=' ', ind2=' ', controlfield_value='',
                     subfields=None, field_position_global=None,
                     field_position_local=None):
    """
    Add a new field into the record.

    If field_position_global or field_position_local is specified then
    this method will insert the new field at the desired position.
    Otherwise a global field position will be computed in order to
    insert the field at the best position (first we try to keep the
    order of the tags and then we insert the field at the end of the
    fields with the same tag).

    If both field_position_global and field_position_local are present,
    then field_position_local takes precedence.

    :param rec: the record data structure
    :param tag: the tag of the field to be added
    :param ind1: the first indicator
    :param ind2: the second indicator
    :param controlfield_value: the value of the controlfield
    :param subfields: the subfields (a list of tuples (code, value))
    :param field_position_global: the global field position (record wise)
    :param field_position_local: the local field position (tag wise)
    :return: the global field position of the newly inserted field or -1 if the
             operation failed
    """
    error = _validate_record_field_positions_global(rec)
    if error:
        # FIXME one should write a message here
        pass

    # Clean the parameters.
    if subfields is None:
        subfields = []
    ind1, ind2 = _wash_indicators(ind1, ind2)

    if controlfield_value and (ind1 != ' ' or ind2 != ' ' or subfields):
        return -1

    # Detect field number to be used for insertion:
    # Dictionaries for uniqueness.
    tag_field_positions_global = {}.fromkeys([field[4]
                                              for field in rec.get(tag, [])])
    all_field_positions_global = {}.fromkeys([field[4]
                                              for fields in rec.values()
                                              for field in fields])

    if field_position_global is None and field_position_local is None:
        # Let's determine the global field position of the new field.
        if tag in rec:
            try:
                field_position_global = max([field[4] for field in rec[tag]]) \
                    + 1
            except IndexError:
                if tag_field_positions_global:
                    field_position_global = max(tag_field_positions_global) + 1
                elif all_field_positions_global:
                    field_position_global = max(all_field_positions_global) + 1
                else:
                    field_position_global = 1
        else:
            if tag in ('FMT', 'FFT', 'BDR', 'BDM'):
                # Add the new tag to the end of the record.
                if tag_field_positions_global:
                    field_position_global = max(tag_field_positions_global) + 1
                elif all_field_positions_global:
                    field_position_global = max(all_field_positions_global) + 1
                else:
                    field_position_global = 1
            else:
                # Insert the tag in an ordered way by selecting the
                # right global field position.
                immediate_lower_tag = '000'
                for rec_tag in rec:
                    if (tag not in ('FMT', 'FFT', 'BDR', 'BDM') and
                            rec[rec_tag] and
                            immediate_lower_tag < rec_tag < tag):
                        immediate_lower_tag = rec_tag

                if immediate_lower_tag == '000':
                    field_position_global = 1
                else:
                    field_position_global = rec[immediate_lower_tag][-1][4] + 1

        field_position_local = len(rec.get(tag, []))
        _shift_field_positions_global(rec, field_position_global, 1)
    elif field_position_local is not None:
        if tag in rec:
            if field_position_local >= len(rec[tag]):
                field_position_global = rec[tag][-1][4] + 1
            else:
                field_position_global = rec[tag][field_position_local][4]
            _shift_field_positions_global(rec, field_position_global, 1)
        else:
            if all_field_positions_global:
                field_position_global = max(all_field_positions_global) + 1
            else:
                # Empty record.
                field_position_global = 1
    elif field_position_global is not None:
        # If the user chose an existing global field position, shift all the
        # global field positions greater than the input global field position.
        if tag not in rec:
            if all_field_positions_global:
                field_position_global = max(all_field_positions_global) + 1
            else:
                field_position_global = 1
            field_position_local = 0
        elif field_position_global < min(tag_field_positions_global):
            field_position_global = min(tag_field_positions_global)
            _shift_field_positions_global(rec, min(tag_field_positions_global),
                                          1)
            field_position_local = 0
        elif field_position_global > max(tag_field_positions_global):
            field_position_global = max(tag_field_positions_global) + 1
            _shift_field_positions_global(rec,
                                          max(tag_field_positions_global) + 1,
                                          1)
            field_position_local = len(rec.get(tag, []))
        else:
            if field_position_global in tag_field_positions_global:
                _shift_field_positions_global(rec, field_position_global, 1)

            field_position_local = 0
            for position, field in enumerate(rec[tag]):
                if field[4] == field_position_global + 1:
                    field_position_local = position

    # Create the new field.
    newfield = (subfields, ind1, ind2, str(controlfield_value),
                field_position_global)
    rec.setdefault(tag, []).insert(field_position_local, newfield)

    # Return new field number:
    return field_position_global