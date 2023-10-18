def _qsub_collate_and_launch(self, output_dir, error_dir, job_names):
        """
        The method that actually runs qsub to invoke the python
        process with the necessary commands to trigger the next
        collation step and next block of jobs.
        """

        job_name = "%s_%s_collate_%d" % (self.batch_name,
                                         self.job_timestamp,
                                         self.collate_count)

        overrides = [("-e",error_dir), ('-N',job_name), ("-o",output_dir),
                     ('-hold_jid',','.join(job_names))]

        resume_cmds =["import os, pickle, lancet",
                      ("pickle_path = os.path.join(%r, 'qlauncher.pkl')"
                       % self.root_directory),
                      "launcher = pickle.load(open(pickle_path,'rb'))",
                      "launcher.collate_and_launch()"]

        cmd_args = [self.command.executable,
                    '-c', ';'.join(resume_cmds)]
        popen_args = self._qsub_args(overrides, cmd_args)

        p = subprocess.Popen(popen_args, stdout=subprocess.PIPE)
        (stdout, stderr) = p.communicate()

        self.debug(stdout)
        if p.poll() != 0:
            raise EnvironmentError("qsub command exit with code: %d" % p.poll())

        self.collate_count += 1
        self.message("Invoked qsub for next batch.")
        return job_name