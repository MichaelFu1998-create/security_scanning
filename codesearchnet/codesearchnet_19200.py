def stage(self, name, pipeline_counter=None):
        """Helper to instantiate a :class:`gocd.api.stage.Stage` object

        Args:
            name: The name of the stage
            pipeline_counter:

        Returns:

        """
        return Stage(
            self.server,
            pipeline_name=self.name,
            stage_name=name,
            pipeline_counter=pipeline_counter,
        )