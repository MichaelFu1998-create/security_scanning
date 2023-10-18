def shutdown(self, hub=True, targets='all', block=False):
        """Shutdown the executor, including all workers and controllers.

        This is not implemented.

        Kwargs:
            - hub (Bool): Whether the hub should be shutdown, Default:True,
            - targets (list of ints| 'all'): List of block id's to kill, Default:'all'
            - block (Bool): To block for confirmations or not

        Raises:
             NotImplementedError
        """

        logger.info("Attempting HighThroughputExecutor shutdown")
        # self.outgoing_q.close()
        # self.incoming_q.close()
        self.queue_proc.terminate()
        logger.info("Finished HighThroughputExecutor shutdown attempt")
        return True