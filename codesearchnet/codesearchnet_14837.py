def build_payload(ipaddress,
                  event_type,
                  event_time=None,
                  start_time=None,
                  end_time=None):
    """Method builds a payload out of the passed arguments.

    Parameters:
        `ipaddress`: the models.IPAddress object
        `event_type`: USAGE,CREATE,DELETE,SUSPEND,or UNSUSPEND
        `start_time`: startTime for cloudfeeds
        `end_time`: endTime for cloudfeeds
    Returns a dictionary suitable to notify billing.
    Message types mapping to cloud feeds for references:
        ip.exists       - USAGE
        ip.add          - CREATE
        ip.delete       - DELETE
        ip.associate    - UP
        ip.disassociate  - DOWN
    Refer to: http://rax.io/cf-api for more details.
    """
    # This is the common part of all message types
    payload = {
        'event_type': unicode(event_type),
        'tenant_id': unicode(ipaddress.used_by_tenant_id),
        'ip_address': unicode(ipaddress.address_readable),
        'ip_version': int(ipaddress.version),
        'ip_type': unicode(ipaddress.address_type),
        'id': unicode(ipaddress.id)
    }

    # Depending on the message type add the appropriate fields
    if event_type == IP_EXISTS:
        if start_time is None or end_time is None:
            raise ValueError('IP_BILL: {} start_time/end_time cannot be empty'
                             .format(event_type))
        payload.update({
            'startTime': unicode(convert_timestamp(start_time)),
            'endTime': unicode(convert_timestamp(end_time))
        })
    elif event_type in [IP_ADD, IP_DEL, IP_ASSOC, IP_DISASSOC]:
        if event_time is None:
            raise ValueError('IP_BILL: {}: event_time cannot be NULL'
                             .format(event_type))
        payload.update({
            'eventTime': unicode(convert_timestamp(event_time)),
            'subnet_id': unicode(ipaddress.subnet_id),
            'network_id': unicode(ipaddress.network_id),
            'public': True if ipaddress.network_id == PUBLIC_NETWORK_ID
            else False,
        })
    else:
        raise ValueError('IP_BILL: bad event_type: {}'.format(event_type))

    return payload