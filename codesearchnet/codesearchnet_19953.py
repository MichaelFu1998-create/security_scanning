def _qsub_block(self, output_dir, error_dir, tid_specs):
        """
        This method handles static argument specifiers and cases where
        the dynamic specifiers cannot be queued before the arguments
        are known.
        """
        processes = []
        job_names = []

        for (tid, spec) in tid_specs:
            job_name = "%s_%s_tid_%d" % (self.batch_name, self.job_timestamp, tid)
            job_names.append(job_name)
            cmd_args = self.command(
                    self.command._formatter(spec),
                    tid, self._launchinfo)

            popen_args = self._qsub_args([("-e",error_dir), ('-N',job_name), ("-o",output_dir)],
                                        cmd_args)
            p = subprocess.Popen(popen_args, stdout=subprocess.PIPE)
            (stdout, stderr) = p.communicate()

            self.debug(stdout)
            if p.poll() != 0:
                raise EnvironmentError("qsub command exit with code: %d" % p.poll())

            processes.append(p)

        self.message("Invoked qsub for %d commands" % len(processes))
        if (self.reduction_fn is not None) or self.dynamic:
            self._qsub_collate_and_launch(output_dir, error_dir, job_names)