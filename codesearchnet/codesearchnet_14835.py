def do_notify(context, event_type, payload):
    """Generic Notifier.

    Parameters:
        - `context`: session context
        - `event_type`: the event type to report, i.e. ip.usage
        - `payload`: dict containing the payload to send
    """
    LOG.debug('IP_BILL: notifying {}'.format(payload))

    notifier = n_rpc.get_notifier('network')
    notifier.info(context, event_type, payload)