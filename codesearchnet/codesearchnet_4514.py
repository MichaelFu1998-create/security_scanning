def update_parent(self, fut):
        """Add a callback to the parent to update the state.

        This handles the case where the user has called result on the AppFuture
        before the parent exists.
        """
        self.parent = fut

        try:
            fut.add_done_callback(self.parent_callback)
        except Exception as e:
            logger.error("add_done_callback got an exception {} which will be ignored".format(e))