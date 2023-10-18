def add_job_to_context(context, job_id):
    """Adds job to neutron context for use later."""
    db_job = db_api.async_transaction_find(
        context, id=job_id, scope=db_api.ONE)
    if not db_job:
        return
    context.async_job = {"job": v._make_job_dict(db_job)}