def run_mainloop_with(self, target):
        """Start the OS's main loop to process asyncronous BLE events and then
        run the specified target function in a background thread.  Target
        function should be a function that takes no parameters and optionally
        return an integer response code.  When the target function stops
        executing or returns with value then the main loop will be stopped and
        the program will exit with the returned code.

        Note that an OS main loop is required to process asyncronous BLE events
        and this function is provided as a convenience for writing simple tools
        and scripts that don't need to be full-blown GUI applications.  If you
        are writing a GUI application that has a main loop (a GTK glib main loop
        on Linux, or a Cocoa main loop on OSX) then you don't need to call this
        function.
        """
        # Create background thread to run user code.
        self._user_thread = threading.Thread(target=self._user_thread_main,
                                             args=(target,))
        self._user_thread.daemon = True
        self._user_thread.start()
        # Run main loop.  This call will never return!
        try:
            AppHelper.runConsoleEventLoop(installInterrupt=True)
        except KeyboardInterrupt:
            AppHelper.stopEventLoop()
            sys.exit(0)