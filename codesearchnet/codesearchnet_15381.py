def validate_model(cursor, model):
    """Validates the model using a series of checks on bits of the data."""
    # Check the license is one valid for publication.
    _validate_license(model)
    _validate_roles(model)

    # Other required metadata includes: title, summary
    required_metadata = ('title', 'summary',)
    for metadata_key in required_metadata:
        if model.metadata.get(metadata_key) in [None, '', []]:
            raise exceptions.MissingRequiredMetadata(metadata_key)

    # Ensure that derived-from values are either None
    # or point at a live record in the archive.
    _validate_derived_from(cursor, model)

    # FIXME Valid language code?

    # Are the given 'subjects'
    _validate_subjects(cursor, model)