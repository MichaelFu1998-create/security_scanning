def delete_scalingip(context, id):
    """Deallocate a scaling IP.

    :param context: neutron api request context.
    :param id: id of the scaling ip
    """
    LOG.info('delete_scalingip %s for tenant %s' % (id, context.tenant_id))
    _delete_flip(context, id, ip_types.SCALING)