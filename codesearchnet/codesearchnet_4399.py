def _start_local_queue_process(self):
        """ TODO: docstring """

        comm_q = Queue(maxsize=10)
        self.queue_proc = Process(target=interchange.starter,
                                  args=(comm_q,),
                                  kwargs={"client_ports": (self.outgoing_q.port,
                                                           self.incoming_q.port),
                                          "worker_port": self.worker_port,
                                          "worker_port_range": self.worker_port_range
                                          # TODO: logdir and logging level
                                          })
        self.queue_proc.start()

        try:
            worker_port = comm_q.get(block=True, timeout=120)
            logger.debug(
                "Got worker port {} from interchange".format(worker_port))
        except queue.Empty:
            logger.error(
                "Interchange has not completed initialization in 120s. Aborting")
            raise Exception("Interchange failed to start")

        self.worker_task_url = "tcp://{}:{}".format(
            self.address, worker_port)