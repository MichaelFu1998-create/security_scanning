def parent_callback(self, parent_fu):
        """Callback from executor future to update the parent.

        Args:
            - parent_fu (Future): Future returned by the executor along with callback

        Returns:
            - None

        Updates the super() with the result() or exception()
        """
        if parent_fu.done() is True:
            e = parent_fu._exception
            if e:
                super().set_exception(e)
            else:
                super().set_result(self.file_obj)
        return