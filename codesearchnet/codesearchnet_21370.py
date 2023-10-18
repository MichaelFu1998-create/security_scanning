def wait(self):
        """
            This function waits for the relay and responding processes to exit.
            Captures KeyboardInterrupt to shutdown these processes.
        """
        try:
            self.relay.wait()
            self.responder.wait()
        except KeyboardInterrupt:
            print_notification("Stopping")
        finally:
            self.terminate_processes()