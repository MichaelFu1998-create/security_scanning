def _make_job_dict(job):
    """Creates the view for a job while calculating progress.

    Since a root job does not have a transaction id (TID) it will return its
    id as the TID.
    """
    body = {"id": job.get('id'),
            "action": job.get('action'),
            "completed": job.get('completed'),
            "tenant_id": job.get('tenant_id'),
            "created_at": job.get('created_at'),
            "transaction_id": job.get('transaction_id'),
            "parent_id": job.get('parent_id', None)}
    if not body['transaction_id']:
        body['transaction_id'] = job.get('id')
    completed = 0
    for sub in job.subtransactions:
        if sub.get('completed'):
            completed += 1
    pct = 100 if job.get('completed') else 0
    if len(job.subtransactions) > 0:
        pct = float(completed) / len(job.subtransactions) * 100.0
    body['transaction_percent'] = int(pct)
    body['completed_subtransactions'] = completed
    body['subtransactions'] = len(job.subtransactions)
    return body