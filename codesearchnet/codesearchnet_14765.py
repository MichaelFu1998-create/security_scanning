def update_ip_address(context, id, ip_address):
    """Due to NCP-1592 ensure that address_type cannot change after update."""
    LOG.info("update_ip_address %s for tenant %s" % (id, context.tenant_id))
    ports = []
    if 'ip_address' not in ip_address:
        raise n_exc.BadRequest(resource="ip_addresses",
                               msg="Invalid request body.")
    with context.session.begin():
        db_address = db_api.ip_address_find(context, id=id, scope=db_api.ONE)
        if not db_address:
            raise q_exc.IpAddressNotFound(addr_id=id)
        iptype = db_address.address_type
        if iptype == ip_types.FIXED and not CONF.QUARK.ipaddr_allow_fixed_ip:
            raise n_exc.BadRequest(
                resource="ip_addresses",
                msg="Fixed ips cannot be updated using this interface.")

        reset = ip_address['ip_address'].get('reset_allocation_time', False)
        if reset and db_address['deallocated'] == 1:
            if context.is_admin:
                LOG.info("IP's deallocated time being manually reset")
                db_address['deallocated_at'] = _get_deallocated_override()
            else:
                msg = "Modification of reset_allocation_time requires admin"
                raise webob.exc.HTTPForbidden(detail=msg)

        port_ids = ip_address['ip_address'].get('port_ids', None)

        if port_ids is not None and not port_ids:
            raise n_exc.BadRequest(
                resource="ip_addresses",
                msg="Cannot be updated with empty port_id list")

        if iptype == ip_types.SHARED:
            has_owner = db_address.has_any_shared_owner()

        if port_ids:
            if iptype == ip_types.FIXED and len(port_ids) > 1:
                raise n_exc.BadRequest(
                    resource="ip_addresses",
                    msg="Fixed ips cannot be updated with more than one port.")

            _raise_if_shared_and_enabled(ip_address, db_address)
            ports = db_api.port_find(context, tenant_id=context.tenant_id,
                                     id=port_ids, scope=db_api.ALL)
            # NOTE(name): could be considered inefficient because we're
            # converting to a list to check length. Maybe revisit
            if len(ports) != len(port_ids):
                raise n_exc.PortNotFound(port_id=port_ids)

            validate_and_fetch_segment(ports, db_address["network_id"])
            validate_port_ip_quotas(context, db_address.network_id, ports)

            if iptype == ip_types.SHARED and has_owner:
                for assoc in db_address.associations:
                    pid = assoc.port_id
                    if pid not in port_ids and 'none' != assoc.service:
                        raise q_exc.PortRequiresDisassociation()

            LOG.info("Updating IP address, %s, to only be used by the"
                     "following ports:  %s" % (db_address.address_readable,
                                               [p.id for p in ports]))
            new_address = db_api.update_port_associations_for_ip(context,
                                                                 ports,
                                                                 db_address)
        elif iptype == ip_types.SHARED and has_owner:
            raise q_exc.PortRequiresDisassociation()
        elif 'deallocated' in ip_address['ip_address']\
                and context.is_admin:
            # Verify no port associations
            if len(db_address.associations) != 0:
                exc_msg = ("IP %s cannot be deallocated or allocated while"
                           " still associated with ports: %s"
                           % (db_address['address_readable'],
                              db_address.associations))
                raise q_exc.ActionNotAuthorized(msg=exc_msg)

            # NOTE: If an admin, allow a user to set deallocated to false
            # in order to reserve a deallocated IP. Alternatively, allow them
            # reverse that choice if a mistake was made.
            if ip_address['ip_address']['deallocated'] == 'False':
                db_address['deallocated'] = False
            else:
                db_address['deallocated'] = True
            return v._make_ip_dict(db_address, context.is_admin)
        else:
            ipam_driver.deallocate_ip_address(context, db_address)
            return v._make_ip_dict(db_address, context.is_admin)
    return v._make_ip_dict(new_address, context.is_admin)