def _user_thread_main(self, target):
        """Main entry point for the thread that will run user's code."""
        try:
            # Wait for GLib main loop to start running before starting user code.
            while True:
                if self._gobject_mainloop is not None and self._gobject_mainloop.is_running():
                    # Main loop is running, we should be ready to make bluez DBus calls.
                    break
                # Main loop isn't running yet, give time back to other threads.
                time.sleep(0)
            # Run user's code.
            self._return_code = target()
            # Assume good result (0 return code) if none is returned.
            if self._return_code is None:
                self._return_code = 0
            # Signal the main loop to exit.
            self._gobject_mainloop.quit()
        except Exception as ex:
            # Something went wrong.  Raise the exception on the main thread to
            # exit.
            self._exception = sys.exc_info()
            self._gobject_mainloop.quit()