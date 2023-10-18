def _perform_async_update_rule(context, id, db_sg_group, rule_id, action):
    """Updates a SG rule async and return the job information.

    Only happens if the security group has associated ports. If the async
    connection fails the update continues (legacy mode).
    """
    rpc_reply = None
    sg_rpc = sg_rpc_api.QuarkSGAsyncProcessClient()
    ports = db_api.sg_gather_associated_ports(context, db_sg_group)
    if len(ports) > 0:
        rpc_reply = sg_rpc.start_update(context, id, rule_id, action)
        if rpc_reply:
            job_id = rpc_reply['job_id']
            job_api.add_job_to_context(context, job_id)
        else:
            LOG.error("Async update failed. Is the worker running?")