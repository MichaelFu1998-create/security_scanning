def recv_task_request_from_workers(self):
        """ Receives 1 task request from MPI comm

        Returns:
        --------
            worker_rank: worker_rank id
        """
        info = MPI.Status()
        comm.recv(source=MPI.ANY_SOURCE, tag=TASK_REQUEST_TAG, status=info)
        worker_rank = info.Get_source()
        logger.info("Received task request from worker:{}".format(worker_rank))
        return worker_rank