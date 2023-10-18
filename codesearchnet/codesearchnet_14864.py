def update_ports_for_sg(self, context, portid, jobid):
        """Updates the ports through redis."""
        port = db_api.port_find(context, id=portid, scope=db_api.ONE)
        if not port:
            LOG.warning("Port not found")
            return
        net_driver = port_api._get_net_driver(port.network, port=port)
        base_net_driver = port_api._get_net_driver(port.network)
        sg_list = [sg for sg in port.security_groups]

        success = False
        error = None
        retries = 3
        retry_delay = 2
        for retry in xrange(retries):
            try:
                net_driver.update_port(context, port_id=port["backend_key"],
                                       mac_address=port["mac_address"],
                                       device_id=port["device_id"],
                                       base_net_driver=base_net_driver,
                                       security_groups=sg_list)
                success = True
                error = None
                break
            except Exception as error:
                LOG.warning("Could not connect to redis, but retrying soon")
                time.sleep(retry_delay)
        status_str = ""
        if not success:
            status_str = "Port %s update failed after %d tries. Error: %s" % (
                portid, retries, error)
        update_body = dict(completed=True, status=status_str)
        update_body = dict(job=update_body)
        job_api.update_job(context.elevated(), jobid, update_body)