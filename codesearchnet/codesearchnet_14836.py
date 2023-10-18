def notify(context, event_type, ipaddress, send_usage=False, *args, **kwargs):
    """Method to send notifications.

    We must send USAGE when a public IPv4 address is deallocated or a FLIP is
    associated.
    Parameters:
        - `context`: the context for notifier
        - `event_type`: the event type for IP allocate, deallocate, associate,
        disassociate
        - `ipaddress`: the ipaddress object to notify about
    Returns:
        nothing
    Notes: this may live in the billing module
    """
    if (event_type == IP_ADD and not CONF.QUARK.notify_ip_add) or \
       (event_type == IP_DEL and not CONF.QUARK.notify_ip_delete) or \
       (event_type == IP_ASSOC and not CONF.QUARK.notify_flip_associate) or \
       (event_type == IP_DISASSOC and not CONF.QUARK.notify_flip_disassociate)\
       or (event_type == IP_EXISTS and not CONF.QUARK.notify_ip_exists):
        LOG.debug('IP_BILL: notification {} is disabled by config'.
                  format(event_type))
        return

    # Do not send notifications when we are undoing due to an error
    if 'rollback' in kwargs and kwargs['rollback']:
        LOG.debug('IP_BILL: not sending notification because we are in undo')
        return

    # ip.add needs the allocated_at time.
    # All other events need the current time.
    ts = ipaddress.allocated_at if event_type == IP_ADD else _now()
    payload = build_payload(ipaddress, event_type, event_time=ts)

    # Send the notification with the payload
    do_notify(context, event_type, payload)

    # When we deallocate an IP or associate a FLIP we must send
    # a usage message to billing.
    # In other words when we supply end_time we must send USAGE to billing
    # immediately.
    # Our billing period is 24 hrs. If the address was allocated after midnight
    # send the start_time as as. If the address was allocated yesterday, then
    # send midnight as the start_time.
    # Note: if allocated_at is empty we assume today's midnight.
    if send_usage:
        if ipaddress.allocated_at is not None and \
           ipaddress.allocated_at >= _midnight_today():
            start_time = ipaddress.allocated_at
        else:
            start_time = _midnight_today()
        payload = build_payload(ipaddress,
                                IP_EXISTS,
                                start_time=start_time,
                                end_time=ts)
        do_notify(context, IP_EXISTS, payload)