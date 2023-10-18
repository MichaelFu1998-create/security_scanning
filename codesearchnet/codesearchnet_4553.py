def start(self):
        """Create the Interchange process and connect to it.
        """
        self.outgoing_q = zmq_pipes.TasksOutgoing("127.0.0.1", self.interchange_port_range)
        self.incoming_q = zmq_pipes.ResultsIncoming("127.0.0.1", self.interchange_port_range)
        self.command_client = zmq_pipes.CommandClient("127.0.0.1", self.interchange_port_range)

        self.is_alive = True

        self._executor_bad_state = threading.Event()
        self._executor_exception = None
        self._queue_management_thread = None
        self._start_queue_management_thread()
        self._start_local_queue_process()

        logger.debug("Created management thread: {}".format(self._queue_management_thread))

        if self.provider:
            self.initialize_scaling()
        else:
            self._scaling_enabled = False
            logger.debug("Starting HighThroughputExecutor with no provider")