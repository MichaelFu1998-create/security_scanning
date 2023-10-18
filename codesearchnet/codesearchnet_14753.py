def _update_flip(context, flip_id, ip_type, requested_ports):
    """Update a flip based IPAddress

    :param context: neutron api request context.
    :param flip_id: id of the flip or scip
    :param ip_type: ip_types.FLOATING | ip_types.SCALING
    :param requested_ports: dictionary of the structure:
    {"port_id": "<id of port>", "fixed_ip": "<fixed ip address>"}
    :return: quark.models.IPAddress
    """
    # This list will hold flips that require notifications.
    # Using sets to avoid dups, if any.
    notifications = {
        billing.IP_ASSOC: set(),
        billing.IP_DISASSOC: set()
    }

    context.session.begin()
    try:
        flip = db_api.floating_ip_find(context, id=flip_id, scope=db_api.ONE)
        if not flip:
            if ip_type == ip_types.SCALING:
                raise q_exc.ScalingIpNotFound(id=flip_id)
            raise q_exc.FloatingIpNotFound(id=flip_id)
        current_ports = flip.ports

        # Determine what ports are being removed, being added, and remain
        req_port_ids = [request_port.get('port_id')
                        for request_port in requested_ports]
        curr_port_ids = [curr_port.id for curr_port in current_ports]
        added_port_ids = [port_id for port_id in req_port_ids
                          if port_id and port_id not in curr_port_ids]
        removed_port_ids = [port_id for port_id in curr_port_ids
                            if port_id not in req_port_ids]
        remaining_port_ids = set(curr_port_ids) - set(removed_port_ids)

        # Validations just for floating ip types
        if (ip_type == ip_types.FLOATING and curr_port_ids and
                curr_port_ids == req_port_ids):
            d = dict(flip_id=flip_id, port_id=curr_port_ids[0])
            raise q_exc.PortAlreadyAssociatedToFloatingIp(**d)
        if (ip_type == ip_types.FLOATING and
                not curr_port_ids and not req_port_ids):
            raise q_exc.FloatingIpUpdateNoPortIdSupplied()

        # Validate that GW IP is not in use on the NW.
        flip_subnet = v._make_subnet_dict(flip.subnet)
        for added_port_id in added_port_ids:
            port = _get_port(context, added_port_id)
            nw = port.network
            nw_ports = v._make_ports_list(nw.ports)
            fixed_ips = [ip.get('ip_address') for p in nw_ports
                         for ip in p.get('fixed_ips')]

            gw_ip = flip_subnet.get('gateway_ip')
            if gw_ip in fixed_ips:
                port_with_gateway_ip = None
                for port in nw_ports:
                    for ip in port.get('fixed_ips'):
                        if gw_ip in ip.get('ip_address'):
                            port_with_gateway_ip = port
                            break
                port_id = port_with_gateway_ip.get('id')
                network_id = port_with_gateway_ip.get('network_id')
                raise q_exc.FixedIpAllocatedToGatewayIp(port_id=port_id,
                                                        network_id=network_id)
        port_fixed_ips = {}

        # Keep the ports and fixed ips that have not changed
        for port_id in remaining_port_ids:
            port = db_api.port_find(context, id=port_id, scope=db_api.ONE)
            fixed_ip = _get_flip_fixed_ip_by_port_id(flip, port_id)
            port_fixed_ips[port_id] = {'port': port, 'fixed_ip': fixed_ip}

        # Disassociate the ports and fixed ips from the flip that were
        # associated to the flip but are not anymore
        for port_id in removed_port_ids:
            port = db_api.port_find(context, id=port_id, scope=db_api.ONE)
            flip = db_api.port_disassociate_ip(context, [port], flip)
            notifications[billing.IP_DISASSOC].add(flip)
            fixed_ip = _get_flip_fixed_ip_by_port_id(flip, port_id)
            if fixed_ip:
                flip = db_api.floating_ip_disassociate_fixed_ip(
                    context, flip, fixed_ip)

        # Validate the new ports with the flip and associate the new ports
        # and fixed ips with the flip
        for port_id in added_port_ids:
            port = db_api.port_find(context, id=port_id, scope=db_api.ONE)
            if not port:
                raise n_exc.PortNotFound(port_id=port_id)
            if any(ip for ip in port.ip_addresses
                   if (ip.get('address_type') == ip_types.FLOATING)):
                raise q_exc.PortAlreadyContainsFloatingIp(port_id=port_id)
            if any(ip for ip in port.ip_addresses
                   if (ip.get('address_type') == ip_types.SCALING)):
                raise q_exc.PortAlreadyContainsScalingIp(port_id=port_id)
            fixed_ip = _get_next_available_fixed_ip(port)
            LOG.info('new fixed ip: %s' % fixed_ip)
            if not fixed_ip:
                raise q_exc.NoAvailableFixedIpsForPort(port_id=port_id)
            port_fixed_ips[port_id] = {'port': port, 'fixed_ip': fixed_ip}
            flip = db_api.port_associate_ip(context, [port], flip, [port_id])
            notifications[billing.IP_ASSOC].add(flip)
            flip = db_api.floating_ip_associate_fixed_ip(context, flip,
                                                         fixed_ip)

        flip_driver = registry.DRIVER_REGISTRY.get_driver()
        # If there are not any remaining ports and no new ones are being added,
        # remove the floating ip from unicorn
        if not remaining_port_ids and not added_port_ids:
            flip_driver.remove_floating_ip(flip)
        # If new ports are being added but there previously was not any ports,
        # then register a new floating ip with the driver because it is
        # assumed it does not exist
        elif added_port_ids and not curr_port_ids:
            flip_driver.register_floating_ip(flip, port_fixed_ips)
        else:
            flip_driver.update_floating_ip(flip, port_fixed_ips)
        context.session.commit()
    except Exception:
        context.session.rollback()
        raise

    # Send notifications for possible associate/disassociate events
    for notif_type, flip_set in notifications.iteritems():
        for flip in flip_set:
            billing.notify(context, notif_type, flip)

    # NOTE(blogan): ORM does not seem to update the model to the real state
    # of the database, so I'm doing an explicit refresh for now.
    context.session.refresh(flip)
    return flip