def initialize_scaling(self):
        """ Compose the launch command and call the scale_out

        This should be implemented in the child classes to take care of
        executor specific oddities.
        """
        debug_opts = "--debug" if self.worker_debug else ""
        max_workers = "" if self.max_workers == float('inf') else "--max_workers={}".format(self.max_workers)

        worker_logdir = "{}/{}".format(self.run_dir, self.label)
        if self.worker_logdir_root is not None:
            worker_logdir = "{}/{}".format(self.worker_logdir_root, self.label)

        l_cmd = self.launch_cmd.format(debug=debug_opts,
                                       prefetch_capacity=self.prefetch_capacity,
                                       task_url=self.worker_task_url,
                                       result_url=self.worker_result_url,
                                       cores_per_worker=self.cores_per_worker,
                                       max_workers=max_workers,
                                       nodes_per_block=self.provider.nodes_per_block,
                                       heartbeat_period=self.heartbeat_period,
                                       heartbeat_threshold=self.heartbeat_threshold,
                                       poll_period=self.poll_period,
                                       logdir=worker_logdir)
        self.launch_cmd = l_cmd
        logger.debug("Launch command: {}".format(self.launch_cmd))

        self._scaling_enabled = self.provider.scaling_enabled
        logger.debug("Starting HighThroughputExecutor with provider:\n%s", self.provider)
        if hasattr(self.provider, 'init_blocks'):
            try:
                self.scale_out(blocks=self.provider.init_blocks)
            except Exception as e:
                logger.error("Scaling out failed: {}".format(e))
                raise e