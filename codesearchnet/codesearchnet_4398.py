def start(self):
        """Create the Interchange process and connect to it.
        """
        self.outgoing_q = zmq_pipes.TasksOutgoing(
            "127.0.0.1", self.interchange_port_range)
        self.incoming_q = zmq_pipes.ResultsIncoming(
            "127.0.0.1", self.interchange_port_range)

        self.is_alive = True

        self._queue_management_thread = None
        self._start_queue_management_thread()
        self._start_local_queue_process()

        logger.debug("Created management thread: {}"
                     .format(self._queue_management_thread))

        if self.provider:
            # debug_opts = "--debug" if self.worker_debug else ""
            l_cmd = self.launch_cmd.format(  # debug=debug_opts,
                task_url=self.worker_task_url,
                workers_per_node=self.workers_per_node,
                logdir="{}/{}".format(self.run_dir, self.label))
            self.launch_cmd = l_cmd
            logger.debug("Launch command: {}".format(self.launch_cmd))

            self._scaling_enabled = self.provider.scaling_enabled
            logger.debug(
                "Starting LowLatencyExecutor with provider:\n%s", self.provider)
            if hasattr(self.provider, 'init_blocks'):
                try:
                    for i in range(self.provider.init_blocks):
                        block = self.provider.submit(
                            self.launch_cmd, 1, self.workers_per_node)
                        logger.debug("Launched block {}:{}".format(i, block))
                        if not block:
                            raise(ScalingFailed(self.provider.label,
                                                "Attempts to provision nodes via provider has failed"))
                        self.blocks.extend([block])

                except Exception as e:
                    logger.error("Scaling out failed: {}".format(e))
                    raise e
        else:
            self._scaling_enabled = False
            logger.debug("Starting LowLatencyExecutor with no provider")