def record_extract_dois(record):
    """Return the DOI(s) of the record."""
    record_dois = []
    tag = "024"
    ind1 = "7"
    ind2 = "_"
    subfield_source_code = "2"
    subfield_value_code = "a"
    identifiers_fields = record_get_field_instances(record, tag, ind1, ind2)
    for identifer_field in identifiers_fields:
        if 'doi' in [val.lower() for val in
                     field_get_subfield_values(identifer_field,
                                               subfield_source_code)]:
            record_dois.extend(
                field_get_subfield_values(
                    identifer_field,
                    subfield_value_code))
    return record_dois