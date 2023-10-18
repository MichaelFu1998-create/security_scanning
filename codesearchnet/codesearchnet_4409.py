def start(self):
        """ Start the Manager process.

        The worker loops on this:

        1. If the last message sent was older than heartbeat period we send a heartbeat
        2.


        TODO: Move task receiving to a thread
        """

        self.comm.Barrier()
        logger.debug("Manager synced with workers")

        self._kill_event = threading.Event()
        self._task_puller_thread = threading.Thread(target=self.pull_tasks,
                                                    args=(self._kill_event,))
        self._result_pusher_thread = threading.Thread(target=self.push_results,
                                                      args=(self._kill_event,))
        self._task_puller_thread.start()
        self._result_pusher_thread.start()

        start = None

        result_counter = 0
        task_recv_counter = 0
        task_sent_counter = 0

        logger.info("Loop start")
        while not self._kill_event.is_set():
            time.sleep(LOOP_SLOWDOWN)

            # In this block we attempt to probe MPI for a set amount of time,
            # and if we have exhausted all available MPI events, we move on
            # to the next block. The timer and counter trigger balance
            # fairness and responsiveness.
            timer = time.time() + 0.05
            counter = min(10, comm.size)
            while time.time() < timer:
                info = MPI.Status()

                if counter > 10:
                    logger.debug("Hit max mpi events per round")
                    break

                if not self.comm.Iprobe(status=info):
                    logger.debug("Timer expired, processed {} mpi events".format(counter))
                    break
                else:
                    tag = info.Get_tag()
                    logger.info("Message with tag {} received".format(tag))

                    counter += 1
                    if tag == RESULT_TAG:
                        result = self.recv_result_from_workers()
                        self.pending_result_queue.put(result)
                        result_counter += 1

                    elif tag == TASK_REQUEST_TAG:
                        worker_rank = self.recv_task_request_from_workers()
                        self.ready_worker_queue.put(worker_rank)

                    else:
                        logger.error("Unknown tag {} - ignoring this message and continuing".format(tag))

            available_worker_cnt = self.ready_worker_queue.qsize()
            available_task_cnt = self.pending_task_queue.qsize()
            logger.debug("[MAIN] Ready workers: {} Ready tasks: {}".format(available_worker_cnt,
                                                                           available_task_cnt))
            this_round = min(available_worker_cnt, available_task_cnt)
            for i in range(this_round):
                worker_rank = self.ready_worker_queue.get()
                task = self.pending_task_queue.get()
                comm.send(task, dest=worker_rank, tag=worker_rank)
                task_sent_counter += 1
                logger.debug("Assigning worker:{} task:{}".format(worker_rank, task['task_id']))

            if not start:
                start = time.time()

            logger.debug("Tasks recvd:{} Tasks dispatched:{} Results recvd:{}".format(
                task_recv_counter, task_sent_counter, result_counter))
            # print("[{}] Received: {}".format(self.identity, msg))
            # time.sleep(random.randint(4,10)/10)

        self._task_puller_thread.join()
        self._result_pusher_thread.join()

        self.task_incoming.close()
        self.result_outgoing.close()
        self.context.term()

        delta = time.time() - start
        logger.info("mpi_worker_pool ran for {} seconds".format(delta))