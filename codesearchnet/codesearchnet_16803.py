def deposit_minter(record_uuid, data):
    """Mint a deposit identifier.

    A PID with the following characteristics is created:

    .. code-block:: python

        {
            "object_type": "rec",
            "object_uuid": record_uuid,
            "pid_value": "<new-pid-value>",
            "pid_type": "depid",
        }

    The following deposit meta information are updated:

    .. code-block:: python

        deposit['_deposit'] = {
            "id": "<new-pid-value>",
            "status": "draft",
        }

    :param record_uuid: Record UUID.
    :param data: Record content.
    :returns: A :class:`invenio_pidstore.models.PersistentIdentifier` object.
    """
    provider = DepositProvider.create(
        object_type='rec',
        object_uuid=record_uuid,
        pid_value=uuid.uuid4().hex,
    )
    data['_deposit'] = {
        'id': provider.pid.pid_value,
        'status': 'draft',
    }
    return provider.pid