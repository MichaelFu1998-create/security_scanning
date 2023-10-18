def file_serializer(obj):
    """Serialize a object.

    :param obj: A :class:`invenio_files_rest.models.ObjectVersion` instance.
    :returns: A dictionary with the fields to serialize.
    """
    return {
        "id": str(obj.file_id),
        "filename": obj.key,
        "filesize": obj.file.size,
        "checksum": obj.file.checksum,
    }