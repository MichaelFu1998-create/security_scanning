def create_job(context, body):
    """Creates a job with support for subjobs.

    If parent_id is not in the body:
    * the job is considered a parent job
    * it will have a NULL transaction id
    * its transaction id == its id
    * all subjobs will use its transaction id as theirs

    Else:
    * the job is a sub job
    * the parent id is the id passed in
    * the transaction id is the root of the job tree
    """
    LOG.info("create_job for tenant %s" % context.tenant_id)

    if not context.is_admin:
        raise n_exc.NotAuthorized()
    job = body.get('job')
    if 'parent_id' in job:
        parent_id = job['parent_id']
        if not parent_id:
            raise q_exc.JobNotFound(job_id=parent_id)
        parent_job = db_api.async_transaction_find(
            context, id=parent_id, scope=db_api.ONE)
        if not parent_job:
            raise q_exc.JobNotFound(job_id=parent_id)
        tid = parent_id
        if parent_job.get('transaction_id'):
            tid = parent_job.get('transaction_id')
        job['transaction_id'] = tid

    if not job:
        raise n_exc.BadRequest(resource="job", msg="Invalid request body.")
    with context.session.begin(subtransactions=True):
        new_job = db_api.async_transaction_create(context, **job)
    return v._make_job_dict(new_job)