def wait(self):
        """ Wait and join the child process. 
            The return value of the function call is returned.
            If any exception occurred it is wrapped and raised.
        """
        e, r = self.result.get()
        self.slave.join()
        self.slave = None
        self.result = None
        if isinstance(e, Exception):
            raise SlaveException(e, r)
        return r