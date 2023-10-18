def close(self):
        ''' Close the network connection and perform any other required cleanup

            Note:
                Auto closed when using goose as a context manager or when garbage collected '''
        if self.fetcher is not None:
            self.shutdown_network()
        self.finalizer.atexit = False