def run(self, stdout=sys.stdout, stderr=sys.stderr):
    '''
    Runs this SyncEngine by executing one of the following functions
    (as controlled by command-line options or stored parameters):

    * Display local pending changes.
    * Describe local configuration.
    * Run an HTTP server and engage server-side mode.
    * Connect to a remote SyncML peer and engage client-side mode.

    NOTE: when running in the first two modes, all database interactions
    are rolled back in order to keep the SyncEngine idempotent.
    '''
    if self.options.local or self.options.describe:
      context, adapter = self._makeAdapter()
      if self.options.describe:
        self.describe(stdout)
        adapter.describe(stdout)
      self.dbsession.rollback()
      return 0
    if self.options.server:
      return self._runServer(stdout, stderr)
    return self._runClient(stdout, stderr)