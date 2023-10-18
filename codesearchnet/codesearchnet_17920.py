def remove_handler(self, name):
        """
        Remove handler from the logging system if present already.
        Available handlers are currently: ['console-bw', 'console-color', 'rotating-log']
        """
        if name in self.handlers:
            self.log.removeHandler(self.handlers[name])