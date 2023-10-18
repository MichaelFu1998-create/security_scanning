def _command_server(self, kill_event):
        """ Command server to run async command to the interchange
        """
        logger.debug("[COMMAND] Command Server Starting")
        while not kill_event.is_set():
            try:
                command_req = self.command_channel.recv_pyobj()
                logger.debug("[COMMAND] Received command request: {}".format(command_req))
                if command_req == "OUTSTANDING_C":
                    outstanding = self.pending_task_queue.qsize()
                    for manager in self._ready_manager_queue:
                        outstanding += len(self._ready_manager_queue[manager]['tasks'])
                    reply = outstanding

                elif command_req == "WORKERS":
                    num_workers = 0
                    for manager in self._ready_manager_queue:
                        num_workers += self._ready_manager_queue[manager]['worker_count']
                    reply = num_workers
                elif command_req == "MANAGERS":
                    reply = []
                    for manager in self._ready_manager_queue:
                        resp = {'manager': manager.decode('utf-8'),
                                'block_id': self._ready_manager_queue[manager]['block_id'],
                                'worker_count': self._ready_manager_queue[manager]['worker_count'],
                                'tasks': len(self._ready_manager_queue[manager]['tasks']),
                                'active': self._ready_manager_queue[manager]['active']}
                        reply.append(resp)

                elif command_req.startswith("HOLD_WORKER"):
                    cmd, s_manager = command_req.split(';')
                    manager = s_manager.encode('utf-8')
                    logger.info("[CMD] Received HOLD_WORKER for {}".format(manager))
                    if manager in self._ready_manager_queue:
                        self._ready_manager_queue[manager]['active'] = False
                        reply = True
                    else:
                        reply = False

                elif command_req == "SHUTDOWN":
                    logger.info("[CMD] Received SHUTDOWN command")
                    kill_event.set()
                    reply = True

                else:
                    reply = None

                logger.debug("[COMMAND] Reply: {}".format(reply))
                self.command_channel.send_pyobj(reply)

            except zmq.Again:
                logger.debug("[COMMAND] is alive")
                continue