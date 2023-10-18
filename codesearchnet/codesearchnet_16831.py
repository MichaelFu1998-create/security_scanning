def json_files_serializer(objs, status=None):
    """JSON Files Serializer.

    :parma objs: A list of:class:`invenio_files_rest.models.ObjectVersion`
        instances.
    :param status: A HTTP Status. (Default: ``None``)
    :returns: A Flask response with JSON data.
    :rtype: :py:class:`flask.Response`.
    """
    files = [file_serializer(obj) for obj in objs]
    return make_response(json.dumps(files), status)