def submit(self, cmd_string, blocksize, tasks_per_node, job_name="parsl"):
        """ Submit a job
        Args:
             - cmd_string  :(String) - Name of the container to initiate
             - blocksize   :(float) - Number of replicas
             - tasks_per_node (int) : command invocations to be launched per node

        Kwargs:
             - job_name (String): Name for job, must be unique
        Returns:
             - None: At capacity, cannot provision more
             - job_id: (string) Identifier for the job
        """
        if not self.resources:
            cur_timestamp = str(time.time() * 1000).split(".")[0]
            job_name = "{0}-{1}".format(job_name, cur_timestamp)

            if not self.deployment_name:
                deployment_name = '{}-deployment'.format(job_name)
            else:
                deployment_name = '{}-{}-deployment'.format(self.deployment_name,
                                                            cur_timestamp)

            formatted_cmd = template_string.format(command=cmd_string,
                                                   worker_init=self.worker_init)

            self.deployment_obj = self._create_deployment_object(job_name,
                                                                 self.image,
                                                                 deployment_name,
                                                                 cmd_string=formatted_cmd,
                                                                 replicas=self.init_blocks,
                                                                 volumes=self.persistent_volumes)
            logger.debug("Deployment name :{}".format(deployment_name))
            self._create_deployment(self.deployment_obj)
            self.resources[deployment_name] = {'status': 'RUNNING',
                                               'pods': self.init_blocks}

        return deployment_name