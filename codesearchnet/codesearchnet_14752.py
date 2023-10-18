def _create_flip(context, flip, port_fixed_ips):
    """Associates the flip with ports and creates it with the flip driver

    :param context: neutron api request context.
    :param flip: quark.db.models.IPAddress object representing a floating IP
    :param port_fixed_ips: dictionary of the structure:
    {"<id of port>": {"port": <quark.db.models.Port>,
     "fixed_ip": "<fixed ip address>"}}
    :return: None
    """
    if port_fixed_ips:
        context.session.begin()
        try:
            ports = [val['port'] for val in port_fixed_ips.values()]
            flip = db_api.port_associate_ip(context, ports, flip,
                                            port_fixed_ips.keys())

            for port_id in port_fixed_ips:
                fixed_ip = port_fixed_ips[port_id]['fixed_ip']
                flip = db_api.floating_ip_associate_fixed_ip(context, flip,
                                                             fixed_ip)

            flip_driver = registry.DRIVER_REGISTRY.get_driver()

            flip_driver.register_floating_ip(flip, port_fixed_ips)
            context.session.commit()
        except Exception:
            context.session.rollback()
            raise

    # alexm: Notify from this method for consistency with _delete_flip
    billing.notify(context, billing.IP_ASSOC, flip)