def update_sg(self, context, sg, rule_id, action):
        """Begins the async update process."""
        db_sg = db_api.security_group_find(context, id=sg, scope=db_api.ONE)
        if not db_sg:
            return None
        with context.session.begin():
            job_body = dict(action="%s sg rule %s" % (action, rule_id),
                            resource_id=rule_id,
                            tenant_id=db_sg['tenant_id'])
            job_body = dict(job=job_body)
            job = job_api.create_job(context.elevated(), job_body)
            rpc_client = QuarkSGAsyncProducerClient()
            try:
                rpc_client.populate_subtasks(context, sg, job['id'])
            except om_exc.MessagingTimeout:
                LOG.error("Failed to create subtasks. Rabbit running?")
                return None
        return {"job_id": job['id']}