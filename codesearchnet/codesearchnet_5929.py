def delete(self, batch_id):
        """
        Stops a batch request from running. Since only one batch request is
        run at a time, this can be used to cancel a long running request. The
        results of any completed operations will not be available after this
        call.

        :param batch_id: The unique id for the batch operation.
        :type batch_id: :py:class:`str`
        """
        self.batch_id = batch_id
        self.operation_status = None
        return self._mc_client._delete(url=self._build_path(batch_id))