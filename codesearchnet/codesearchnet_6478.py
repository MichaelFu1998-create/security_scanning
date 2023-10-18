def _user_thread_main(self, target):
        """Main entry point for the thread that will run user's code."""
        try:
            # Run user's code.
            return_code = target()
            # Assume good result (0 return code) if none is returned.
            if return_code is None:
                return_code = 0
            # Call exit on the main thread when user code has finished.
            AppHelper.callAfter(lambda: sys.exit(return_code))
        except Exception as ex:
            # Something went wrong.  Raise the exception on the main thread to exit.
            AppHelper.callAfter(self._raise_error, sys.exc_info())