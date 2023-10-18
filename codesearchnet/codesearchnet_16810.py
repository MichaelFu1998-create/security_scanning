def can_elasticsearch(record):
    """Check if a given record is indexed.

    :param record: A record object.
    :returns: If the record is indexed returns `True`, otherwise `False`.
    """
    search = request._methodview.search_class()
    search = search.get_record(str(record.id))
    return search.count() == 1