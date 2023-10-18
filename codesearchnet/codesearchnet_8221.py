def stop(self):
        """
        Stop the Runner if it's running.
        Called as a classmethod, stop the running instance if any.
        """
        if self.is_running:
            log.info('Stopping')
            self.is_running = False
            self.__class__._INSTANCE = None

            try:
                self.thread and self.thread.stop()
            except:
                log.error('Error stopping thread')
                traceback.print_exc()
            self.thread = None
            return True