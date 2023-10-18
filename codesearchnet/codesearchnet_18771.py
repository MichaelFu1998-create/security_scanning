def create_records(marcxml, verbose=CFG_BIBRECORD_DEFAULT_VERBOSE_LEVEL,
                   correct=CFG_BIBRECORD_DEFAULT_CORRECT, parser='',
                   keep_singletons=CFG_BIBRECORD_KEEP_SINGLETONS):
    """
    Create a list of records from the marcxml description.

    :returns: a list of objects initiated by the function create_record().
              Please see that function's docstring.
    """
    # Use the DOTALL flag to include newlines.
    regex = re.compile('<record.*?>.*?</record>', re.DOTALL)
    record_xmls = regex.findall(marcxml)

    return [create_record(record_xml, verbose=verbose, correct=correct,
            parser=parser, keep_singletons=keep_singletons)
            for record_xml in record_xmls]