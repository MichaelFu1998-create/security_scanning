def populate_subtasks(self, context, sg, parent_job_id):
        """Produces a list of ports to be updated async."""
        db_sg = db_api.security_group_find(context, id=sg, scope=db_api.ONE)
        if not db_sg:
            return None
        ports = db_api.sg_gather_associated_ports(context, db_sg)
        if len(ports) == 0:
            return {"ports": 0}
        for port in ports:
            job_body = dict(action="update port %s" % port['id'],
                            tenant_id=db_sg['tenant_id'],
                            resource_id=port['id'],
                            parent_id=parent_job_id)
            job_body = dict(job=job_body)
            job = job_api.create_job(context.elevated(), job_body)
            rpc_consumer = QuarkSGAsyncConsumerClient()
            try:
                rpc_consumer.update_port(context, port['id'], job['id'])
            except om_exc.MessagingTimeout:
                # TODO(roaet): Not too sure what can be done here other than
                # updating the job as a failure?
                LOG.error("Failed to update port. Rabbit running?")
        return None