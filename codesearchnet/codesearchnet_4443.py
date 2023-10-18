def start(self):
        """ TODO: docstring """
        logger.info("Starting interchange")
        # last = time.time()

        while True:
            # active_flag = False
            socks = dict(self.poller.poll(1))

            if socks.get(self.task_incoming) == zmq.POLLIN:
                message = self.task_incoming.recv_multipart()
                logger.debug("Got new task from client")
                self.worker_messages.send_multipart(message)
                logger.debug("Sent task to worker")
                # active_flag = True
                # last = time.time()

            if socks.get(self.worker_messages) == zmq.POLLIN:
                message = self.worker_messages.recv_multipart()
                logger.debug("Got new result from worker")
                # self.result_outgoing.send_multipart(message)
                self.result_outgoing.send_multipart(message[1:])

                logger.debug("Sent result to client")