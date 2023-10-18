def json_file_response(obj=None, pid=None, record=None, status=None):
    """JSON Files/File serializer.

    :param obj: A :class:`invenio_files_rest.models.ObjectVersion` instance or
        a :class:`invenio_records_files.api.FilesIterator` if it's a list of
        files.
    :param pid: PID value. (not used)
    :param record: The record metadata. (not used)
    :param status: The HTTP status code.
    :returns: A Flask response with JSON data.
    :rtype: :py:class:`flask.Response`.
    """
    from invenio_records_files.api import FilesIterator

    if isinstance(obj, FilesIterator):
        return json_files_serializer(obj, status=status)
    else:
        return json_file_serializer(obj, status=status)