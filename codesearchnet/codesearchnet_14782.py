def delete_subnet(context, id):
    """Delete a subnet.

    : param context: neutron api request context
    : param id: UUID representing the subnet to delete.
    """
    LOG.info("delete_subnet %s for tenant %s" % (id, context.tenant_id))
    with context.session.begin():
        subnet = db_api.subnet_find(context, id=id, scope=db_api.ONE)
        if not subnet:
            raise n_exc.SubnetNotFound(subnet_id=id)

        if not context.is_admin:
            if STRATEGY.is_provider_network(subnet.network_id):
                if subnet.tenant_id == context.tenant_id:
                    # A tenant can't delete subnets on provider network
                    raise n_exc.NotAuthorized(subnet_id=id)
                else:
                    # Raise a NotFound here because the foreign tenant
                    # does not have to know about other tenant's subnet
                    # existence.
                    raise n_exc.SubnetNotFound(subnet_id=id)

        _delete_subnet(context, subnet)