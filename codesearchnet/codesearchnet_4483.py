def submit(self, command, blocksize, tasks_per_node, job_name="parsl.auto"):
        ''' Submits the command onto an Local Resource Manager job of blocksize parallel elements.
        Submit returns an ID that corresponds to the task that was just submitted.

        If tasks_per_node <  1:
             1/tasks_per_node is provisioned

        If tasks_per_node == 1:
             A single node is provisioned

        If tasks_per_node >  1 :
             tasks_per_node * blocksize number of nodes are provisioned.

        Args:
             - command  :(String) Commandline invocation to be made on the remote side.
             - blocksize   :(float) - Not really used for local
             - tasks_per_node (int) : command invocations to be launched per node

        Kwargs:
             - job_name (String): Name for job, must be unique

        Returns:
             - None: At capacity, cannot provision more
             - job_id: (string) Identifier for the job

        '''

        job_name = "{0}.{1}".format(job_name, time.time())

        # Set script path
        script_path = "{0}/{1}.sh".format(self.script_dir, job_name)
        script_path = os.path.abspath(script_path)

        wrap_command = self.worker_init + '\n' + self.launcher(command, tasks_per_node, self.nodes_per_block)

        self._write_submit_script(wrap_command, script_path)

        job_id = None
        proc = None
        remote_pid = None
        if (self.move_files is None and not isinstance(self.channel, LocalChannel)) or (self.move_files):
            logger.debug("Moving start script")
            script_path = self.channel.push_file(script_path, self.channel.script_dir)

        if not isinstance(self.channel, LocalChannel):
            logger.debug("Launching in remote mode")
            # Bash would return until the streams are closed. So we redirect to a outs file
            cmd = 'bash {0} &> {0}.out & \n echo "PID:$!" '.format(script_path)
            retcode, stdout, stderr = self.channel.execute_wait(cmd, self.cmd_timeout)
            for line in stdout.split('\n'):
                if line.startswith("PID:"):
                    remote_pid = line.split("PID:")[1].strip()
                    job_id = remote_pid
            if job_id is None:
                logger.warning("Channel failed to start remote command/retrieve PID")
        else:

            try:
                job_id, proc = self.channel.execute_no_wait('bash {0}'.format(script_path), self.cmd_timeout)
            except Exception as e:
                logger.debug("Channel execute failed for: {}, {}".format(self.channel, e))
                raise

        self.resources[job_id] = {'job_id': job_id, 'status': 'RUNNING',
                                  'blocksize': blocksize,
                                  'remote_pid': remote_pid,
                                  'proc': proc}

        return job_id