def create_record(marcxml=None, verbose=CFG_BIBRECORD_DEFAULT_VERBOSE_LEVEL,
                  correct=CFG_BIBRECORD_DEFAULT_CORRECT, parser='',
                  sort_fields_by_indicators=False,
                  keep_singletons=CFG_BIBRECORD_KEEP_SINGLETONS):
    """Create a record object from the marcxml description.

    Uses the lxml parser.

    The returned object is a tuple (record, status_code, list_of_errors),
    where status_code is 0 when there are errors, 1 when no errors.

    The return record structure is as follows::

        Record := {tag : [Field]}
        Field := (Subfields, ind1, ind2, value)
        Subfields := [(code, value)]

    .. code-block:: none

                                    .--------.
                                    | record |
                                    '---+----'
                                        |
               .------------------------+------------------------------------.
               |record['001']           |record['909']        |record['520'] |
               |                        |                     |              |
        [list of fields]           [list of fields]     [list of fields]    ...
               |                        |                     |
               |               .--------+--+-----------.      |
               |               |           |           |      |
               |[0]            |[0]        |[1]       ...     |[0]
          .----+------.  .-----+-----.  .--+--------.     .---+-------.
          | Field 001 |  | Field 909 |  | Field 909 |     | Field 520 |
          '-----------'  '-----+-----'  '--+--------'     '---+-------'
               |               |           |                  |
              ...              |          ...                ...
                               |
                    .----------+-+--------+------------.
                    |            |        |            |
                    |[0]         |[1]     |[2]         |
          [list of subfields]   'C'      '4'          ...
                    |
               .----+---------------+------------------------+
               |                    |                        |
        ('a', 'value')              |            ('a', 'value for another a')
                     ('b', 'value for subfield b')

    :param marcxml: an XML string representation of the record to create
    :param verbose: the level of verbosity: 0 (silent), 1-2 (warnings),
                    3(strict:stop when errors)
    :param correct: 1 to enable correction of marcxml syntax. Else 0.
    :return: a tuple (record, status_code, list_of_errors), where status
             code is 0 where there are errors, 1 when no errors
    """
    if marcxml is None:
        return {}
    try:
        rec = _create_record_lxml(marcxml, verbose, correct,
                                  keep_singletons=keep_singletons)
    except InvenioBibRecordParserError as ex1:
        return (None, 0, str(ex1))

    if sort_fields_by_indicators:
        _record_sort_by_indicators(rec)

    errs = []
    if correct:
        # Correct the structure of the record.
        errs = _correct_record(rec)

    return (rec, int(not errs), errs)