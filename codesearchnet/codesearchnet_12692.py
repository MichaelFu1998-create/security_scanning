def clean_fields(fields, ignored_value_indices, transforms):
    """
    Sometimes, NetMHC* has fields that are only populated sometimes, which results
    in different count/indexing of the fields when that happens.

    We handle this by looking for particular strings at particular indices, and
    deleting them.

    Warning: this may result in unexpected behavior sometimes. For example, we
    ignore "SB" and "WB" for NetMHC 3.x output; which also means that any line
    with a key called SB or WB will be ignored.

    Also, sometimes NetMHC* will have fields that we want to modify in some
    consistent way, e.g. NetMHCpan3 has 1-based offsets and all other predictors
    have 0-based offsets (and we rely on 0-based offsets). We handle this using
    a map from field index to transform function.
    """
    cleaned_fields = []
    for i, field in enumerate(fields):
        if field in ignored_value_indices:
            ignored_index = ignored_value_indices[field]

            # Is the value we want to ignore at the index where we'd ignore it?
            if ignored_index == i:
                continue

        # transform this field if the index is in transforms, otherwise leave alone
        cleaned_field = transforms[i](field) if i in transforms else field
        cleaned_fields.append(cleaned_field)
    return cleaned_fields