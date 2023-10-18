def delete_floatingip(context, id):
    """deallocate a floating IP.

    :param context: neutron api request context.
    :param id: id of the floating ip
    """

    LOG.info('delete_floatingip %s for tenant %s' % (id, context.tenant_id))

    _delete_flip(context, id, ip_types.FLOATING)