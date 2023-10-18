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
        # Spin up a background thread to run the target code.
        self._user_thread = threading.Thread(target=self._user_thread_main, args=(target,))
        self._user_thread.daemon = True  # Don't let the user thread block exit.
        self._user_thread.start()
        # Spin up a GLib main loop in the main thread to process async BLE events.
        self._gobject_mainloop = GObject.MainLoop()
        try:
            self._gobject_mainloop.run()  # Doesn't return until the mainloop ends.
        except KeyboardInterrupt:
            self._gobject_mainloop.quit()
            sys.exit(0)
        # Main loop finished.  Check if an exception occured and throw it,
        # otherwise return the status code from the user code.
        if self._exception is not None:
            # Rethrow exception with its original stack trace following advice from:
            # http://nedbatchelder.com/blog/200711/rethrowing_exceptions_in_python.html
            raise_(self._exception[1], None, self._exception[2])
        else:
            sys.exit(self._return_code)