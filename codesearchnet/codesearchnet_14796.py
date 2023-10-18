def delete_job(context, id, **filters):
    """Delete an ip address.

    : param context: neutron api request context
    : param id: UUID representing the ip address to delete.
    """
    LOG.info("delete_ip_address %s for tenant %s" % (id, context.tenant_id))

    if not context.is_admin:
        raise n_exc.NotAuthorized()
    with context.session.begin():
        job = db_api.async_transaction_find(context, id=id, scope=db_api.ONE,
                                            **filters)
        if not job:
            raise q_exc.JobNotFound(job_id=id)
        db_api.async_transaction_delete(context, job)