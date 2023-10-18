def delayed_call(self, delay, function):
        """Schedule function to be called from the main loop after `delay`
        seconds.

        :Parameters:
            - `delay`: seconds to wait
        :Types:
            - `delay`: `float`
        """
        main_loop = self
        handler = []
        class DelayedCallHandler(TimeoutHandler):
            """Wrapper timeout handler class for the delayed call."""
            # pylint: disable=R0903
            @timeout_handler(delay, False)
            def callback(self):
                """Wrapper timeout handler method for the delayed call."""
                try:
                    function()
                finally:
                    main_loop.remove_handler(handler[0])
        handler.append(DelayedCallHandler())
        self.add_handler(handler[0])