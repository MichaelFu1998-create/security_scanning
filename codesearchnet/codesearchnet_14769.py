def update_port_for_ip_address(context, ip_id, id, port):
    """Update values of a port.

    : param context: neutron api request context
    : param ip_id: UUID representing the ip associated with port to update
    : param id: UUID representing the port to update.
    : param port: dictionary with keys indicating fields to update.
        valid keys are those that have a value of True for 'allow_put'
        as listed in the RESOURCE_ATTRIBUTE_MAP object in
        neutron/api/v2/attributes.py.
    """
    LOG.info("update_port %s for tenant %s" % (id, context.tenant_id))
    sanitize_list = ['service']
    with context.session.begin():
        addr = db_api.ip_address_find(context, id=ip_id, scope=db_api.ONE)
        if not addr:
            raise q_exc.IpAddressNotFound(addr_id=ip_id)
        port_db = db_api.port_find(context, id=id, scope=db_api.ONE)
        if not port_db:
            raise q_exc.PortNotFound(port_id=id)
        port_dict = {k: port['port'][k] for k in sanitize_list}

        require_da = False
        service = port_dict.get('service')

        if require_da and _shared_ip_and_active(addr, except_port=id):
            raise q_exc.PortRequiresDisassociation()
        addr.set_service_for_port(port_db, service)
        context.session.add(addr)
    return v._make_port_for_ip_dict(addr, port_db)