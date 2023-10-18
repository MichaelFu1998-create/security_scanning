def cleanup(self):
        """DataFlowKernel cleanup.

        This involves killing resources explicitly and sending die messages to IPP workers.

        If the executors are managed (created by the DFK), then we call scale_in on each of
        the executors and call executor.shutdown. Otherwise, we do nothing, and executor
        cleanup is left to the user.
        """
        logger.info("DFK cleanup initiated")

        # this check won't detect two DFK cleanups happening from
        # different threads extremely close in time because of
        # non-atomic read/modify of self.cleanup_called
        if self.cleanup_called:
            raise Exception("attempt to clean up DFK when it has already been cleaned-up")
        self.cleanup_called = True

        self.log_task_states()

        # Checkpointing takes priority over the rest of the tasks
        # checkpoint if any valid checkpoint method is specified
        if self.checkpoint_mode is not None:
            self.checkpoint()

            if self._checkpoint_timer:
                logger.info("Stopping checkpoint timer")
                self._checkpoint_timer.close()

        # Send final stats
        self.usage_tracker.send_message()
        self.usage_tracker.close()

        logger.info("Terminating flow_control and strategy threads")
        self.flowcontrol.close()

        for executor in self.executors.values():
            if executor.managed:
                if executor.scaling_enabled:
                    job_ids = executor.provider.resources.keys()
                    executor.scale_in(len(job_ids))
                executor.shutdown()

        self.time_completed = datetime.datetime.now()

        if self.monitoring:
            self.monitoring.send(MessageType.WORKFLOW_INFO,
                                 {'tasks_failed_count': self.tasks_failed_count,
                                  'tasks_completed_count': self.tasks_completed_count,
                                  "time_began": self.time_began,
                                  'time_completed': self.time_completed,
                                  'workflow_duration': (self.time_completed - self.time_began).total_seconds(),
                                  'run_id': self.run_id, 'rundir': self.run_dir})

            self.monitoring.close()

        """
        if self.logging_server is not None:
            self.logging_server.terminate()
            self.logging_server.join()

        if self.web_app is not None:
            self.web_app.terminate()
            self.web_app.join()
        """
        logger.info("DFK cleanup complete")