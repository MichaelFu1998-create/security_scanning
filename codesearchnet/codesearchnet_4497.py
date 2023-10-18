def submit(self, command='sleep 1', blocksize=1, tasks_per_node=1, job_name="parsl.auto"):
        """Submit the command onto a freshly instantiated AWS EC2 instance.

        Submit returns an ID that corresponds to the task that was just submitted.

        Parameters
        ----------
        command : str
            Command to be invoked on the remote side.
        blocksize : int
            Number of blocks requested.
        tasks_per_node : int (default=1)
            Number of command invocations to be launched per node
        job_name : str
            Prefix for the job name.

        Returns
        -------
        None or str
            If at capacity, None will be returned. Otherwise, the job identifier will be returned.
        """

        job_name = "parsl.auto.{0}".format(time.time())
        wrapped_cmd = self.launcher(command,
                                    tasks_per_node,
                                    self.nodes_per_block)
        [instance, *rest] = self.spin_up_instance(command=wrapped_cmd, job_name=job_name)

        if not instance:
            logger.error("Failed to submit request to EC2")
            return None

        logger.debug("Started instance_id: {0}".format(instance.instance_id))

        state = translate_table.get(instance.state['Name'], "PENDING")

        self.resources[instance.instance_id] = {
            "job_id": instance.instance_id,
            "instance": instance,
            "status": state
        }

        return instance.instance_id