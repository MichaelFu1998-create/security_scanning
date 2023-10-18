def instance(self, counter=None, pipeline_counter=None):
        """Returns all the information regarding a specific stage run

        See the `Go stage instance documentation`__ for examples.

        .. __: http://api.go.cd/current/#get-stage-instance

        Args:
          counter (int): The stage instance to fetch.
            If falsey returns the latest stage instance from :meth:`history`.
          pipeline_counter (int): The pipeline instance for which to fetch
            the stage. If falsey returns the latest pipeline instance.

        Returns:
          Response: :class:`gocd.api.response.Response` object
        """
        pipeline_counter = pipeline_counter or self.pipeline_counter
        pipeline_instance = None

        if not pipeline_counter:
            pipeline_instance = self.server.pipeline(self.pipeline_name).instance()
            self.pipeline_counter = int(pipeline_instance['counter'])

        if not counter:
            if pipeline_instance is None:
                pipeline_instance = (
                    self.server
                        .pipeline(self.pipeline_name)
                        .instance(pipeline_counter)
                )

            for stages in pipeline_instance['stages']:
                if stages['name'] == self.stage_name:
                    return self.instance(
                        counter=int(stages['counter']),
                        pipeline_counter=pipeline_counter
                    )

        return self._get('/instance/{pipeline_counter:d}/{counter:d}'
                         .format(pipeline_counter=pipeline_counter, counter=counter))