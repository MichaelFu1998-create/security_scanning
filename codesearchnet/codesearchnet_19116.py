def start(self, total):
        '''
        Signal the start of the process.

        Parameters
        ----------
        total : int
            The total number of steps in the process, or None if unknown.
        '''
        self.logger.info(json.dumps(['START', self.name, total]))