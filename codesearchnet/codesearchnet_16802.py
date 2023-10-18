def deposit_fetcher(record_uuid, data):
    """Fetch a deposit identifier.

    :param record_uuid: Record UUID.
    :param data: Record content.
    :returns: A :class:`invenio_pidstore.fetchers.FetchedPID` that contains
        data['_deposit']['id'] as pid_value.
    """
    return FetchedPID(
        provider=DepositProvider,
        pid_type=DepositProvider.pid_type,
        pid_value=str(data['_deposit']['id']),
    )