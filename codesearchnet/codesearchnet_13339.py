def _loop_timeout_cb(self, main_loop):
        """Stops the loop after the time specified in the `loop` call.
        """
        self._anything_done = True
        logger.debug("_loop_timeout_cb() called")
        main_loop.quit()