def submit(self, command, blocksize, tasks_per_node, job_name="parsl.auto"):
        """ Submits the command onto an Local Resource Manager job of blocksize parallel elements.
        Submit returns an ID that corresponds to the task that was just submitted.

        If tasks_per_node <  1 : ! This is illegal. tasks_per_node should be integer

        If tasks_per_node == 1:
             A single node is provisioned

        If tasks_per_node >  1 :
             tasks_per_node * blocksize number of nodes are provisioned.

        Args:
             - command  :(String) Commandline invocation to be made on the remote side.
             - blocksize   :(float)
             - tasks_per_node (int) : command invocations to be launched per node

        Kwargs:
             - job_name (String): Name for job, must be unique

        Returns:
             - None: At capacity, cannot provision more
             - job_id: (string) Identifier for the job

        """

        if self.provisioned_blocks >= self.max_blocks:
            logger.warn("[%s] at capacity, cannot add more blocks now", self.label)
            return None

        # Note: Fix this later to avoid confusing behavior.
        # We should always allocate blocks in integer counts of node_granularity
        if blocksize < self.nodes_per_block:
            blocksize = self.nodes_per_block

        account_opt = '-A {}'.format(self.account) if self.account is not None else ''

        job_name = "parsl.{0}.{1}".format(job_name, time.time())

        script_path = "{0}/{1}.submit".format(self.script_dir, job_name)
        script_path = os.path.abspath(script_path)

        job_config = {}
        job_config["scheduler_options"] = self.scheduler_options
        job_config["worker_init"] = self.worker_init

        logger.debug("Requesting blocksize:%s nodes_per_block:%s tasks_per_node:%s",
                     blocksize, self.nodes_per_block, tasks_per_node)

        # Wrap the command
        job_config["user_script"] = self.launcher(command, tasks_per_node, self.nodes_per_block)

        queue_opt = '-q {}'.format(self.queue) if self.queue is not None else ''

        logger.debug("Writing submit script")
        self._write_submit_script(template_string, script_path, job_name, job_config)

        channel_script_path = self.channel.push_file(script_path, self.channel.script_dir)

        command = 'qsub -n {0} {1} -t {2} {3} {4}'.format(
            self.nodes_per_block, queue_opt, wtime_to_minutes(self.walltime), account_opt, channel_script_path)
        logger.debug("Executing {}".format(command))

        retcode, stdout, stderr = super().execute_wait(command)

        # TODO : FIX this block
        if retcode != 0:
            logger.error("Failed command: {0}".format(command))
            logger.error("Launch failed stdout:\n{0} \nstderr:{1}\n".format(stdout, stderr))

        logger.debug("Retcode:%s STDOUT:%s STDERR:%s", retcode, stdout.strip(), stderr.strip())

        job_id = None

        if retcode == 0:
            # We should be getting only one line back
            job_id = stdout.strip()
            self.resources[job_id] = {'job_id': job_id, 'status': 'PENDING', 'blocksize': blocksize}
        else:
            logger.error("Submission of command to scale_out failed: {0}".format(stderr))
            raise (ScaleOutFailed(self.__class__, "Request to submit job to local scheduler failed"))

        logger.debug("Returning job id : {0}".format(job_id))
        return job_id