def recv_result_from_workers(self):
        """ Receives a results from the MPI worker pool and send it out via 0mq

        Returns:
        --------
            result: task result from the workers
        """
        info = MPI.Status()
        result = self.comm.recv(source=MPI.ANY_SOURCE, tag=RESULT_TAG, status=info)
        logger.debug("Received result from workers: {}".format(result))
        return result