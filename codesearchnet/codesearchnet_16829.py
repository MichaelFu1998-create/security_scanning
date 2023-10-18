def json_serializer(pid, data, *args):
    """Build a JSON Flask response using the given data.

    :param pid: The `invenio_pidstore.models.PersistentIdentifier` of the
        record.
    :param data: The record metadata.
    :returns: A Flask response with JSON data.
    :rtype: :py:class:`flask.Response`.
    """
    if data is not None:
        response = Response(
            json.dumps(data.dumps()),
            mimetype='application/json'
        )
    else:
        response = Response(mimetype='application/json')
    return response