def instance(self, counter=None):
        """Returns all the information regarding a specific pipeline run

        See the `Go pipeline instance documentation`__ for examples.

        .. __: http://api.go.cd/current/#get-pipeline-instance

        Args:
          counter (int): The pipeline instance to fetch.
            If falsey returns the latest pipeline instance from :meth:`history`.

        Returns:
          Response: :class:`gocd.api.response.Response` object
        """
        if not counter:
            history = self.history()
            if not history:
                return history
            else:
                return Response._from_json(history['pipelines'][0])

        return self._get('/instance/{counter:d}'.format(counter=counter))