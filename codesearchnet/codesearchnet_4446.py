def start(self):
        """ Start the worker processes.

        TODO: Move task receiving to a thread
        """
        start = time.time()
        self._kill_event = threading.Event()

        self.procs = {}
        for worker_id in range(self.worker_count):
            p = multiprocessing.Process(target=worker, args=(worker_id,
                                                             self.uid,
                                                             self.pending_task_queue,
                                                             self.pending_result_queue,
                                                             self.ready_worker_queue,
                                                         ))
            p.start()
            self.procs[worker_id] = p

        logger.debug("Manager synced with workers")

        self._task_puller_thread = threading.Thread(target=self.pull_tasks,
                                                    args=(self._kill_event,))
        self._result_pusher_thread = threading.Thread(target=self.push_results,
                                                      args=(self._kill_event,))
        self._task_puller_thread.start()
        self._result_pusher_thread.start()

        logger.info("Loop start")

        # TODO : Add mechanism in this loop to stop the worker pool
        # This might need a multiprocessing event to signal back.
        self._kill_event.wait()
        logger.critical("[MAIN] Received kill event, terminating worker processes")

        self._task_puller_thread.join()
        self._result_pusher_thread.join()
        for proc_id in self.procs:
            self.procs[proc_id].terminate()
            logger.critical("Terminating worker {}:{}".format(self.procs[proc_id],
                                                              self.procs[proc_id].is_alive()))
            self.procs[proc_id].join()
            logger.debug("Worker:{} joined successfully".format(self.procs[proc_id]))

        self.task_incoming.close()
        self.result_outgoing.close()
        self.context.term()
        delta = time.time() - start
        logger.info("process_worker_pool ran for {} seconds".format(delta))
        return