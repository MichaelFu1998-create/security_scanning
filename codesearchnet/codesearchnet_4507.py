def submit(self, command, blocksize, tasks_per_node, job_name="parsl.auto"):
        """Submits the command onto an Local Resource Manager job of blocksize parallel elements.

        example file with the complex case of multiple submits per job:
            Universe =vanilla
            output = out.$(Cluster).$(Process)
            error = err.$(Cluster).$(Process)
            log = log.$(Cluster)
            leave_in_queue = true
            executable = test.sh
            queue 5
            executable = foo
            queue 1

        $ condor_submit test.sub
        Submitting job(s)......
        5 job(s) submitted to cluster 118907.
        1 job(s) submitted to cluster 118908.

        Parameters
        ----------
        command : str
            Command to execute
        blocksize : int
            Number of blocks to request.
        job_name : str
            Job name prefix.
        tasks_per_node : int
            command invocations to be launched per node
        Returns
        -------
        None or str
            None if at capacity and cannot provision more; otherwise the identifier for the job.
        """

        logger.debug("Attempting to launch with blocksize: {}".format(blocksize))
        if self.provisioned_blocks >= self.max_blocks:
            template = "Provider {} is currently using {} blocks while max_blocks is {}; no blocks will be added"
            logger.warn(template.format(self.label, self.provisioned_blocks, self.max_blocks))
            return None

        # Note: Fix this later to avoid confusing behavior.
        # We should always allocate blocks in integer counts of node_granularity
        blocksize = max(self.nodes_per_block, blocksize)

        job_name = "parsl.{0}.{1}".format(job_name, time.time())

        script_path = "{0}/{1}.submit".format(self.script_dir, job_name)
        script_path = os.path.abspath(script_path)
        userscript_path = "{0}/{1}.script".format(self.script_dir, job_name)
        userscript_path = os.path.abspath(userscript_path)

        self.environment["JOBNAME"] = "'{}'".format(job_name)

        job_config = {}
        job_config["job_name"] = job_name
        job_config["submit_script_dir"] = self.channel.script_dir
        job_config["project"] = self.project
        job_config["nodes"] = self.nodes_per_block
        job_config["scheduler_options"] = self.scheduler_options
        job_config["worker_init"] = self.worker_init
        job_config["user_script"] = command
        job_config["tasks_per_node"] = tasks_per_node
        job_config["requirements"] = self.requirements
        job_config["environment"] = ' '.join(['{}={}'.format(key, value) for key, value in self.environment.items()])

        # Move the user script
        # This is where the command should be wrapped by the launchers.
        wrapped_command = self.launcher(command,
                                        tasks_per_node,
                                        self.nodes_per_block)

        with open(userscript_path, 'w') as f:
            f.write(job_config["worker_init"] + '\n' + wrapped_command)

        user_script_path = self.channel.push_file(userscript_path, self.channel.script_dir)
        the_input_files = [user_script_path] + self.transfer_input_files
        job_config["input_files"] = ','.join(the_input_files)
        job_config["job_script"] = os.path.basename(user_script_path)

        # Construct and move the submit script
        self._write_submit_script(template_string, script_path, job_name, job_config)
        channel_script_path = self.channel.push_file(script_path, self.channel.script_dir)

        cmd = "condor_submit {0}".format(channel_script_path)
        retcode, stdout, stderr = super().execute_wait(cmd, 30)
        logger.debug("Retcode:%s STDOUT:%s STDERR:%s", retcode, stdout.strip(), stderr.strip())

        job_id = []

        if retcode == 0:
            for line in stdout.split('\n'):
                if re.match('^[0-9]', line) is not None:
                    cluster = line.split(" ")[5]
                    # We know the first job id ("process" in condor terms) within a
                    # cluster is 0 and we know the total number of jobs from
                    # condor_submit, so we use some list comprehensions to expand
                    # the condor_submit output into job IDs
                    # e.g., ['118907.0', '118907.1', '118907.2', '118907.3', '118907.4', '118908.0']
                    processes = [str(x) for x in range(0, int(line[0]))]
                    job_id += [cluster + process for process in processes]

            self._add_resource(job_id)
        return job_id[0]