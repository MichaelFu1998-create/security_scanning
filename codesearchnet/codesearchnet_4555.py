def _start_local_queue_process(self):
        """ Starts the interchange process locally

        Starts the interchange process locally and uses an internal command queue to
        get the worker task and result ports that the interchange has bound to.
        """
        comm_q = Queue(maxsize=10)
        self.queue_proc = Process(target=interchange.starter,
                                  args=(comm_q,),
                                  kwargs={"client_ports": (self.outgoing_q.port,
                                                           self.incoming_q.port,
                                                           self.command_client.port),
                                          "worker_ports": self.worker_ports,
                                          "worker_port_range": self.worker_port_range,
                                          "logdir": "{}/{}".format(self.run_dir, self.label),
                                          "suppress_failure": self.suppress_failure,
                                          "heartbeat_threshold": self.heartbeat_threshold,
                                          "poll_period": self.poll_period,
                                          "logging_level": logging.DEBUG if self.worker_debug else logging.INFO
                                  },
        )
        self.queue_proc.start()
        try:
            (worker_task_port, worker_result_port) = comm_q.get(block=True, timeout=120)
        except queue.Empty:
            logger.error("Interchange has not completed initialization in 120s. Aborting")
            raise Exception("Interchange failed to start")

        self.worker_task_url = "tcp://{}:{}".format(self.address, worker_task_port)
        self.worker_result_url = "tcp://{}:{}".format(self.address, worker_result_port)