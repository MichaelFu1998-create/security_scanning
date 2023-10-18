def put(self, task_id, buffer):
        """ TODO: docstring """
        task_id_bytes = task_id.to_bytes(4, "little")
        message = [b"", task_id_bytes] + buffer

        self.zmq_socket.send_multipart(message)
        logger.debug("Sent task {}".format(task_id))