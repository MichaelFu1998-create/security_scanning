def _validate_subnet_cidr(context, network_id, new_subnet_cidr):
    """Validate the CIDR for a subnet.

    Verifies the specified CIDR does not overlap with the ones defined
    for the other subnets specified for this network, or with any other
    CIDR if overlapping IPs are disabled.

    """
    if neutron_cfg.cfg.CONF.allow_overlapping_ips:
        return

    try:
        new_subnet_ipset = netaddr.IPSet([new_subnet_cidr])
    except TypeError:
        LOG.exception("Invalid or missing cidr: %s" % new_subnet_cidr)
        raise n_exc.BadRequest(resource="subnet",
                               msg="Invalid or missing cidr")

    filters = {
        'network_id': network_id,
        'shared': [False]
    }
    # Using admin context here, in case we actually share networks later
    subnet_list = db_api.subnet_find(context=context.elevated(), **filters)

    for subnet in subnet_list:
        if (netaddr.IPSet([subnet.cidr]) & new_subnet_ipset):
            # don't give out details of the overlapping subnet
            err_msg = (_("Requested subnet with cidr: %(cidr)s for "
                         "network: %(network_id)s overlaps with another "
                         "subnet") %
                       {'cidr': new_subnet_cidr,
                        'network_id': network_id})
            LOG.error(_("Validation for CIDR: %(new_cidr)s failed - "
                        "overlaps with subnet %(subnet_id)s "
                        "(CIDR: %(cidr)s)"),
                      {'new_cidr': new_subnet_cidr,
                       'subnet_id': subnet.id,
                       'cidr': subnet.cidr})
            raise n_exc.InvalidInput(error_message=err_msg)