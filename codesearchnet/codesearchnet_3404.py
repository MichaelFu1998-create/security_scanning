def run(self):
        """
        Entry point of the Executor; called by workers to start analysis.
        """
        # policy_order=self.policy_order
        # policy=self.policy
        current_state = None
        current_state_id = None

        with WithKeyboardInterruptAs(self.shutdown):
            # notify siblings we are about to start a run
            self._notify_start_run()

            logger.debug("Starting Manticore Symbolic Emulator Worker (pid %d).", os.getpid())
            solver = Z3Solver()
            while not self.is_shutdown():
                try:  # handle fatal errors: exceptions in Manticore
                    try:  # handle external (e.g. solver) errors, and executor control exceptions
                        # select a suitable state to analyze
                        if current_state is None:
                            with self._lock:
                                # notify siblings we are about to stop this run
                                self._notify_stop_run()
                                try:
                                    # Select a single state_id
                                    current_state_id = self.get()
                                    # load selected state from secondary storage
                                    if current_state_id is not None:
                                        self._publish('will_load_state', current_state_id)
                                        current_state = self._workspace.load_state(current_state_id)
                                        self.forward_events_from(current_state, True)
                                        self._publish('did_load_state', current_state, current_state_id)
                                        logger.info("load state %r", current_state_id)
                                    # notify siblings we have a state to play with
                                finally:
                                    self._notify_start_run()

                        # If current_state is still None. We are done.
                        if current_state is None:
                            logger.debug("No more states in the queue, byte bye!")
                            break

                        assert current_state is not None
                        assert current_state.constraints is current_state.platform.constraints

                        # Allows to terminate manticore worker on user request
                        while not self.is_shutdown():
                            if not current_state.execute():
                                break
                        else:
                            # Notify this worker is done
                            self._publish('will_terminate_state', current_state, current_state_id, TerminateState('Shutdown'))
                            current_state = None

                    # Handling Forking and terminating exceptions
                    except Concretize as e:
                        # expression
                        # policy
                        # setstate()
                        logger.debug("Generic state fork on condition")
                        current_state = self.fork(current_state, e.expression, e.policy, e.setstate)

                    except TerminateState as e:
                        # Notify this worker is done
                        self._publish('will_terminate_state', current_state, current_state_id, e)

                        logger.debug("Generic terminate state")
                        if e.testcase:
                            self._publish('internal_generate_testcase', current_state, message=str(e))
                        current_state = None

                    except SolverError as e:
                        # raise
                        import traceback
                        trace = traceback.format_exc()
                        logger.error("Exception: %s\n%s", str(e), trace)

                        # Notify this state is done
                        self._publish('will_terminate_state', current_state, current_state_id, e)

                        if solver.check(current_state.constraints):
                            self._publish('internal_generate_testcase', current_state, message="Solver failed" + str(e))
                        current_state = None

                except (Exception, AssertionError) as e:
                    # raise
                    import traceback
                    trace = traceback.format_exc()
                    logger.error("Exception: %s\n%s", str(e), trace)
                    # Notify this worker is done
                    self._publish('will_terminate_state', current_state, current_state_id, e)
                    current_state = None

            assert current_state is None or self.is_shutdown()

            # notify siblings we are about to stop this run
            self._notify_stop_run()