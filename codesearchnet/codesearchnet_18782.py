def record_delete_subfield(rec, tag, subfield_code, ind1=' ', ind2=' '):
    """Delete all subfields with subfield_code in the record."""
    ind1, ind2 = _wash_indicators(ind1, ind2)

    for field in rec.get(tag, []):
        if field[1] == ind1 and field[2] == ind2:
            field[0][:] = [subfield for subfield in field[0]
                           if subfield_code != subfield[0]]