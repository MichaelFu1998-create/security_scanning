def is_internal_ip(context, prefix=None):
    """
    Return whether the visitor is coming from an internal IP address,
    based on information from the template context.

    The prefix is used to allow different analytics services to have
    different notions of internal addresses.
    """
    try:
        request = context['request']
        remote_ip = request.META.get('HTTP_X_FORWARDED_FOR', '')
        if not remote_ip:
            remote_ip = request.META.get('REMOTE_ADDR', '')
        if not remote_ip:
            return False

        internal_ips = None
        if prefix is not None:
            internal_ips = getattr(settings, '%s_INTERNAL_IPS' % prefix, None)
        if internal_ips is None:
            internal_ips = getattr(settings, 'ANALYTICAL_INTERNAL_IPS', None)
        if internal_ips is None:
            internal_ips = getattr(settings, 'INTERNAL_IPS', None)

        return remote_ip in (internal_ips or [])
    except (KeyError, AttributeError):
        return False