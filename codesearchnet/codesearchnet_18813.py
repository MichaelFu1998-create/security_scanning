def _create_record_lxml(marcxml,
                        verbose=CFG_BIBRECORD_DEFAULT_VERBOSE_LEVEL,
                        correct=CFG_BIBRECORD_DEFAULT_CORRECT,
                        keep_singletons=CFG_BIBRECORD_KEEP_SINGLETONS):
    """
    Create a record object using the LXML parser.

    If correct == 1, then perform DTD validation
    If correct == 0, then do not perform DTD validation

    If verbose == 0, the parser will not give warnings.
    If 1 <= verbose <= 3, the parser will not give errors, but will warn
        the user about possible mistakes (implement me!)
    If verbose > 3 then the parser will be strict and will stop in case of
        well-formedness errors or DTD errors.

    """
    parser = etree.XMLParser(dtd_validation=correct,
                             recover=(verbose <= 3))
    if correct:
        marcxml = '<?xml version="1.0" encoding="UTF-8"?>\n' \
                  '<collection>\n%s\n</collection>' % (marcxml,)
    try:
        tree = etree.parse(StringIO(marcxml), parser)
        # parser errors are located in parser.error_log
        # if 1 <= verbose <=3 then show them to the user?
        # if verbose == 0 then continue
        # if verbose >3 then an exception will be thrown
    except Exception as e:
        raise InvenioBibRecordParserError(str(e))

    record = {}
    field_position_global = 0

    controlfield_iterator = tree.iter(tag='{*}controlfield')
    for controlfield in controlfield_iterator:
        tag = controlfield.attrib.get('tag', '!').encode("UTF-8")
        ind1 = ' '
        ind2 = ' '
        text = controlfield.text
        if text is None:
            text = ''
        else:
            text = text.encode("UTF-8")
        subfields = []
        if text or keep_singletons:
            field_position_global += 1
            record.setdefault(tag, []).append((subfields, ind1, ind2, text,
                                               field_position_global))

    datafield_iterator = tree.iter(tag='{*}datafield')
    for datafield in datafield_iterator:
        tag = datafield.attrib.get('tag', '!').encode("UTF-8")
        ind1 = datafield.attrib.get('ind1', '!').encode("UTF-8")
        ind2 = datafield.attrib.get('ind2', '!').encode("UTF-8")
        if ind1 in ('', '_'):
            ind1 = ' '
        if ind2 in ('', '_'):
            ind2 = ' '
        subfields = []
        subfield_iterator = datafield.iter(tag='{*}subfield')
        for subfield in subfield_iterator:
            code = subfield.attrib.get('code', '!').encode("UTF-8")
            text = subfield.text
            if text is None:
                text = ''
            else:
                text = text.encode("UTF-8")
            if text or keep_singletons:
                subfields.append((code, text))
        if subfields or keep_singletons:
            text = ''
            field_position_global += 1
            record.setdefault(tag, []).append((subfields, ind1, ind2, text,
                                               field_position_global))

    return record