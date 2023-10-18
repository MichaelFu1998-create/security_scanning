def index_deposit_after_publish(sender, action=None, pid=None, deposit=None):
    """Index the record after publishing.

    .. note:: if the record is not published, it doesn't index.

    :param sender: Who send the signal.
    :param action: Action executed by the sender. (Default: ``None``)
    :param pid: PID object. (Default: ``None``)
    :param deposit: Deposit object. (Default: ``None``)
    """
    if action == 'publish':
        _, record = deposit.fetch_published()
        index_record.delay(str(record.id))