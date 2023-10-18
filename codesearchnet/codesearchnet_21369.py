def terminate_processes(self):
        """
            Terminate the processes.
        """
        if self.relay:
            self.relay.terminate()
        if self.responder:
            self.responder.terminate()