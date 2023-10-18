def initialize(self):
        """Initialize the BLE provider.  Must be called once before any other
        calls are made to the provider.
        """
        # Setup the central manager and its delegate.
        self._central_manager = CBCentralManager.alloc()
        self._central_manager.initWithDelegate_queue_options_(self._central_delegate,
                                                              None, None)